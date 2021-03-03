import ujson as json
import lvgl as lv
from lv_colors import lv_colors

MAX_METAWEATHER_ICON = 10
MAX_DAY = 5
try:
    import urequests
except:
    pass

class WeatherApp():
    
    def __init__(self,mainbar):
        try:
            import ulogging as logging
        except:
            import logging
        self.log = logging.getLogger("WeatherApp")
        self.log.setLevel(logging.DEBUG)   
        self.day_index = 0
        self.woeid="784794" #woeid for Zürich
        self.lat = "47.52637"
        self.lon = "9.74882"

        self.retrieved = False
        self.date = []
        self.weather_state_abbr = []
        self.weather_state_name = []
        self.min_temp = []
        self.max_temp = []
        self.humid = []
        self.predic = []
        self.wind_speed = []
        self.wind_direction = []
        self.air_pressure = []
        self.loc = ""
        self.time = ""
        self.icon_data=[None]*MAX_METAWEATHER_ICON
        self.icon_dsc=[None]*MAX_METAWEATHER_ICON
        self.icon_filename={'c':'c_64px',
                            'h':'h_64px',
                            'hc':'hc_64px',
                            'hr':'hr_64px',
                            'lc':'lc_64px',
                            'lr':'lr_64px',
                            's':'s_64px',
                            'sl':'sl_64px',
                            'sn':'sn_64px',
                            't':'t_64px'}

        self.mainbar=mainbar
        self.statusbar=mainbar.gui.statusbar
        self.app = mainbar.app
        
        self.tile_num = mainbar.add_app_tile( 1, 1, "weather app" )
        self.log.debug("tile number for main tile: %d",self.tile_num)
        
        self.log.debug("registering weather app")
        app=self.app.register("weather","lc_64px",self.enter_weather_app_event_cb)
        
        try:
            self.get_forecast()
            self.log.info("Reading weather forecast from metaweather.com")
        except:
            self.log.info("Reading weather forecast from file metaweather.json")
            self.read_forecast_from_file()

        #
        # create the icons
        #
        keys = list(self.icon_filename.keys())
        for key in keys:
            self.log.debug("Key: %s"%key)
            index = keys.index(key)
            (self.icon_data[index],self.icon_dsc[index]) = self.get_icon(self.icon_filename[key])
        self.main_page(self.tile_num)
        self.widget = mainbar.gui.widget
        self.add_widget()
        
    def get_forecast(self):
        url = "https://www.metaweather.com/api/location/%s/"%self.woeid
        response =  urequests.get(url)
        if response.status_code == 200: # query successful
            # write response to file for testing
            # print(response.text)
            # parse JSON
            data = response.json()
            # print(data)
            response.close()
            # dump the data to a file
            with open('json/metaweather.json', 'w') as json_file:
                json.dump(data, json_file)
            self.decode(data)
        else:
            self.log.error("Query failed, error code was: %d"%response.status_code)

    def decode(self,data):
        self.loc = (data["title"])[:18]
        self.time = data["time"]
        for i in range(MAX_DAY+1):
            w_data = data["consolidated_weather"][i]
            self.date.append(w_data["applicable_date"])
            self.weather_state_name.append(w_data["weather_state_name"])
            self.min_temp.append(float(w_data["min_temp"]))
            self.max_temp.append(float(w_data["max_temp"]))
            self.humid.append(int(w_data["humidity"]))
            self.predic.append(int(w_data["predictability"]))
            self.wind_direction.append(w_data["wind_direction_compass"])
            self.air_pressure.append(w_data["air_pressure"])
            self.weather_state_abbr.append(w_data["weather_state_abbr"])
            self.wind_speed.append(w_data["wind_speed"]*1.609) # convert to kph
        self.location = data["title"]
        self.log.debug("Location: %s"%self.location)
                
    def print_weather_info(self):
        for i in range(MAX_DAY+1):
            output_str = "Date: {0} [{1}%], State: {2}, Temp: {3}/{4} *C, Humid: {5}\n State Abbreviation: {6} Airpressure: {7}, Wind direction: {8}"
            self.log.debug(output_str.format(self.date[i], self.predic[i], self.weather_state_name[i], self.max_temp[i], self.min_temp[i],
                                    self.humid[i], self.weather_state_abbr[i], self.air_pressure[i],self.wind_direction[i]))
            
    def read_forecast_from_file(self):
        with open('json/metaweather.json') as f:
            data = json.load(f)
            self.decode(data)

    def get_icon(self,filename):

        try:
            sdl_filename = 'images/' + filename + "_argb8888.bin"
            self.log.debug('sdl filename: ' + sdl_filename)
            with open(sdl_filename,'rb') as f:
                app_icon_data = f.read()
                self.log.debug(sdl_filename + " successfully read")
        except:
            twatch_filename = 'images/' + filename + "_argb565.bin"
            self.log.debug('t-watch filename: ' + twatch_filename)
            try:
                with open(twatch_filename,'rb') as f:
                    app_icon_data = f.read()
                    self.log.debug(twatch_filename + " successfully read")
                    
            except:
                self.log.error("Could not find image file: " + filename) 

        icon_dsc = lv.img_dsc_t(
            {
                "header": {"always_zero": 0, "w": 64, "h": 64, "cf": lv.img.CF.TRUE_COLOR_ALPHA},
                "data": app_icon_data,
                "data_size": len(app_icon_data),
            }
        )
        return (app_icon_data,icon_dsc)

    def main_page(self,tile_num):
        # create the GUI
        self.weather_app_tile = self.mainbar.get_tile_obj(tile_num);
        weather_style = lv.style_t()
        weather_style.copy(self.mainbar.get_style())
        
        weather_cont = lv.obj(self.weather_app_tile,None)
        weather_cont.set_size(lv.scr_act().get_disp().driver.hor_res,30)
        weather_cont.add_style(lv.cont.PART.MAIN,weather_style)
        
        # create date label and left right buttons
        btn_style = lv.style_t()
        btn_style.copy(weather_style)
        btn_style.set_radius(lv.btn.STATE.RELEASED,2)
        self.left_button = lv.btn(weather_cont,None)
        self.left_button.set_size(25,25)
        self.left_button.add_style(lv.btn.PART.MAIN,btn_style)
        left_label = lv.label(self.left_button,None)
        left_label.set_text(lv.SYMBOL.LEFT)
        self.left_button.align(weather_cont,lv.ALIGN.IN_LEFT_MID,5,0)
        self.left_button.set_hidden(True)
        self.left_button.set_event_cb(self.decrement_day)
        
        self.date_label = lv.label(weather_cont,None)
        self.date_label.set_text(self.date[self.day_index])
        self.date_label.align(weather_cont,lv.ALIGN.CENTER,0,0)
        
        self.right_button = lv.btn(weather_cont,None)
        self.right_button.set_size(25,25)
        self.right_button.add_style(lv.btn.PART.MAIN,btn_style)
        right_label = lv.label(self.right_button,None)
        right_label.set_text(lv.SYMBOL.RIGHT)
        self.right_button.align(weather_cont,lv.ALIGN.IN_RIGHT_MID,-5,0)
        self.right_button.set_event_cb(self.increment_day)

        icon_cont_style = lv.style_t()
        icon_cont_style.copy(weather_style)
        icon_cont_style.set_bg_opa(lv.obj.PART.MAIN, lv.OPA.TRANSP)

        icon_cont = lv.cont(self.weather_app_tile,None)
        icon_cont.set_layout(lv.LAYOUT.COLUMN_LEFT)
        icon_cont.add_style(lv.cont.PART.MAIN,icon_cont_style)
        icon_cont.set_fit(lv.FIT.TIGHT)

        self.icon = lv.img(icon_cont,None)
        key_list = list(self.icon_filename.keys())
        self.log.debug(key_list)
        index = key_list.index(self.weather_state_abbr[self.day_index])
        self.log.debug("index of %s: %d"%(self.weather_state_abbr[self.day_index],index))
        self.icon.set_src(self.icon_dsc[index])
        icon_cont.align(weather_cont,lv.ALIGN.OUT_BOTTOM_LEFT,0,0)
        self.state_label = lv.label(icon_cont,None)
        self.state_label.set_width(100)
        self.state_label.set_text(self.weather_state_name[self.day_index])
        
        info_cont_style = lv.style_t()
        info_cont_style.copy(weather_style)
        info_cont_style.set_pad_top(lv.STATE.DEFAULT,6)
        info_cont_style.set_pad_inner(lv.STATE.DEFAULT,4)
        
        info_cont = lv.cont(self.weather_app_tile,None)
        info_cont.set_size(lv.scr_act().get_disp().driver.hor_res,90)
        info_cont.set_layout(lv.LAYOUT.COLUMN_LEFT)
        info_cont.add_style(lv.cont.PART.MAIN,icon_cont_style)
        info_cont.set_fit(lv.FIT.NONE)
        info_cont.align(icon_cont,lv.ALIGN.OUT_BOTTOM_LEFT,0,0)
        info_cont.add_style(lv.cont.PART.MAIN,info_cont_style)
        
        self.confidence_label = lv.label(info_cont,None)
        self.confidence_label.set_text("Confidence level: {}%".format(self.predic[self.day_index]))
        self.temp_label = lv.label(info_cont,None)
        self.temp_label.set_text("Temp: min: %3.1f°C, max: %3.1f°C"%(self.min_temp[self.day_index],self.max_temp[self.day_index]))
        self.humidity_label = lv.label(info_cont,None)
        self.humidity_label.set_text("Humidity: {}%".format(self.humid[self.day_index]))
        self.pressure_label = lv.label(info_cont,None)
        self.pressure_label.set_text("Air pressure: %d hPa"%self.air_pressure[self.day_index])

        info_cont2 = lv.cont(self.weather_app_tile,None)
        # info_cont2.set_size(140,120)
        info_cont2.set_layout(lv.LAYOUT.COLUMN_LEFT)
        info_cont2.add_style(lv.cont.PART.MAIN,icon_cont_style)
        info_cont2.set_fit(lv.FIT.TIGHT)
        info_cont2.align(icon_cont,lv.ALIGN.OUT_RIGHT_TOP,-5,0)
        info_cont2.add_style(lv.cont.PART.MAIN,info_cont_style)

        self.location_label = lv.label(info_cont2,None)
        self.location_label.set_text("Location: "+self.location)
        self.wind_label = lv.label(info_cont2,None)
        self.wind_label.set_text("Wind:\nspeed: %5.1f kph\ndir: %s"%(self.wind_speed[self.day_index],
                                                                self.wind_direction[self.day_index]))

        exit_btn = lv.imgbtn(self.weather_app_tile,None)
        exit_btn.set_src(lv.btn.STATE.RELEASED,self.mainbar.get_exit_btn_dsc())
        exit_btn.set_src(lv.btn.STATE.PRESSED,self.mainbar.get_exit_btn_dsc())
        exit_btn.set_src(lv.btn.STATE.CHECKED_RELEASED,self.mainbar.get_exit_btn_dsc())
        exit_btn.set_src(lv.btn.STATE.CHECKED_PRESSED,self.mainbar.get_exit_btn_dsc())
        exit_btn.align(self.weather_app_tile,lv.ALIGN.IN_BOTTOM_RIGHT, -10,-10)
        exit_btn.set_event_cb(self.exit_weather_app_event_cb)
        
    def enter_weather_app_event_cb(self,obj,evt):
        if evt == lv.EVENT.CLICKED:
            self.log.debug("enter_aclock_app_event_cb called")
            self.statusbar.hide(True)
            # self.app.hide_indicator( example_app )
            self.mainbar.jump_to_tilenumber(self.tile_num, lv.ANIM.OFF )
            
    def exit_weather_app_event_cb(self,obj,evt):
        if evt == lv.EVENT.CLICKED:
            self.log.debug("exit_aclock_app_event_cb called")
            self.statusbar.hide(False)
            self.mainbar.jump_to_maintile(lv.ANIM.OFF)
    
    def increment_day(self,obj,evt):
        if evt == lv.EVENT.CLICKED:
            self.log.debug("increment_day called")           
            if self.day_index == MAX_DAY:
                return
            self.day_index += 1
            if self.day_index == MAX_DAY:
                self.right_button.set_hidden(True)
            self.left_button.set_hidden(False)
            self.update_day_info()        

    def decrement_day(self,obj,evt):
        if evt == lv.EVENT.CLICKED:
            self.log.debug("decrement_day called")           
            if self.day_index == 0:
                return
            self.day_index -= 1
            if self.day_index == 0:
                self.left_button.set_hidden(True)
            self.right_button.set_hidden(False)
            self.update_day_info()
            
    def update_day_info(self):
        self.log.debug("update_day_info to %d"%self.day_index)
        self.date_label.set_text(self.date[self.day_index])
        key_list = list(self.icon_filename.keys())
        self.log.debug(key_list)
        index = key_list.index(self.weather_state_abbr[self.day_index])
        self.log.debug("index of %s: %d"%(self.weather_state_abbr[self.day_index],index))
        self.icon.set_src(self.icon_dsc[index])
       
        self.state_label.set_text(self.weather_state_name[self.day_index])
        self.confidence_label.set_text("Confidence level: {}%".format(self.predic[self.day_index]))
        self.temp_label.set_text("Temp: min: %3.1f°C, max: %3.1f°C"%(self.min_temp[self.day_index],self.max_temp[self.day_index]))
        self.humidity_label.set_text("Humidity: {}%".format(self.humid[self.day_index]))
        self.pressure_label.set_text("Air pressure: %d hPa"%self.air_pressure[self.day_index])
        self.location_label.set_text("Location: "+self.location)
        self.wind_label.set_text("Wind:\nspeed: %5.1f kph\ndir: %s"%(self.wind_speed[self.day_index],
                                                                self.wind_direction[self.day_index]))

    def add_widget(self):
        key_list = list(self.icon_filename.keys())
        self.log.debug(key_list)
        index = key_list.index(self.weather_state_abbr[0]) # today's weather icon
        self.log.debug("index of %s: %d"%(self.weather_state_abbr[self.day_index],index))
        widget = self.widget.register(self.weather_state_name[self.day_index],self.icon_dsc[index],
                                      self.enter_weather_app_event_cb)
