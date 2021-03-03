#!/opt/bin/lv_micropython -i
import lvgl as lv
from lv_colors import lv_colors
from gui.icon import Icon
import utime as time

class Calendar():

    def __init__(self,mainbar):
        try:
            import ulogging as logging
        except:
            import logging
             
        self.log = logging.getLogger("CalendarApp")
        self.log.setLevel(logging.DEBUG)
        
        self.mainbar=mainbar
        self.statusbar=mainbar.gui.statusbar
        self.app = mainbar.app
        
        self.tile_num = mainbar.add_app_tile( 1, 1, "calendar app" )
        self.log.debug("tile number for main tile: %d",self.tile_num)
        
        self.log.debug("registering calendar app")
        app=self.app.register("calendar","calendar_64px",self.enter_calendar_app_event_cb)
        self.main_page(self.tile_num)
        
    def main_page(self,tile_num):
        self.calendar_tile = self.mainbar.get_tile_obj(tile_num);
        self.calendar_style = lv.style_t()
        self.calendar_style.copy(self.mainbar.get_style())
        
        # create a calendar
        calendar = lv.calendar(self.calendar_tile,None)
        calendar.set_size(200,200)
        calendar.align(self.calendar_tile,lv.ALIGN.CENTER,0,-15)
        calendar.set_event_cb(self.event_handler)
        
        # Make the date number smaller to be sure they fit into their area
        calendar.set_style_local_text_font(lv.calendar.PART.DATE,
                                           lv.STATE.DEFAULT,lv.theme_get_font_small())

        exit_btn = lv.imgbtn(self.calendar_tile,None)        
        exit_btn.set_src(lv.btn.STATE.RELEASED,self.mainbar.get_exit_btn_dsc())
        exit_btn.add_style(lv.imgbtn.PART.MAIN,self.calendar_style)
        exit_btn.align(self.calendar_tile,lv.ALIGN.IN_BOTTOM_LEFT, 10, 0 )
        self.log.debug("setting up exit callback")
        exit_btn.set_event_cb(self.exit_calendar_app_event_cb)
        
        self.calendar_style.set_text_opa(lv.obj.PART.MAIN, lv.OPA.COVER)
        # get current date and time
        today = lv.calendar_date_t()
        if self.mainbar.pcf8563:
            # read time from pcf8563
            localTime = self.mainbar.pcf8563.datetime()
            today.year = localTime[0]+2000
        else:
            now = time.time()
            localTime = time.localtime(now)
            today.year = localTime[0]
            
        today.month = localTime[1]
        today.day= localTime[2]

        calendar.set_today_date(today)
        calendar.set_showed_date(today)
        
    def enter_calendar_app_event_cb(self,obj,evt):
        if evt == lv.EVENT.CLICKED:
            self.log.debug("enter_calendar_app_event_cb called")
            self.statusbar.hide(True)
            # self.app.hide_indicator( example_app )
            self.mainbar.jump_to_tilenumber(self.tile_num, lv.ANIM.OFF )
            
    def exit_calendar_app_event_cb(self,obj,evt):
        if evt == lv.EVENT.CLICKED:
            self.log.debug("exit_calendar_app_event_cb called")
            self.statusbar.hide(False)
            self.mainbar.jump_to_maintile(lv.ANIM.OFF)
    
    def event_handler(self,source,evt):
        if  evt == lv.EVENT.VALUE_CHANGED:
            date = lv.calendar.get_pressed_date(source)
            if date:
                print("Clicked date: %02d.%02d.%02d"%(date.day, date.month, date.year))
