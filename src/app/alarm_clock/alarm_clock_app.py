#!/opt/bin/lv_micropython -i
import lvgl as lv
from lv_colors import lv_colors
from gui.icon import Icon
from micropython import const

DAY_BTN_WIDTH  = 30
DAY_BTN_HEIGHT = 29

class AlarmClock():
    alarm_clock_week_day_2 = ["Su", "Mo", "Tu", "We", "Th", "Fr", "Sa"]
    alarm_clock_week_day_3 = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
    
    def __init__(self,mainbar):
        self.hours =""
        self.minutes = ""
        self.day_button = [None]*7
        self.day_label = [None]*7
        
        try:
            import ulogging as logging
        except:
            import logging
             
        self.log = logging.getLogger("AlarmClockApp")
        self.log.setLevel(logging.DEBUG)

        self.mainbar=mainbar
        self.statusbar=mainbar.gui.statusbar
        self.app = mainbar.app

        self.main_tile_num = mainbar.add_app_tile( 1, 2, "alarmclock app" )
        self.setup_tile_num = self.main_tile_num +1
        self.log.debug("tile number for main tile: %d",self.main_tile_num)
        self.alarm_clock_main_tile = mainbar.get_tile_obj(self.main_tile_num)
        
        self.log.debug("registering alarm_clock app")
        app=self.app.register("alarm\nclock","alarm_clock_64px",self.enter_alarm_clock_main_event_cb)
        # self.app.set_indicator(app,Icon.INDICATOR_OK)
        self.main_page(self.main_tile_num)
        # self.setup_page(self.setup_tile_num)

    def main_page(self,tile_num):
        alarm_clock_main_tile = self.mainbar.get_tile_obj(tile_num);
        alarm_clock_main_style = lv.style_t()
        alarm_clock_main_style.copy(self.mainbar.get_style())
        
        self.activated_cont = lv.obj(alarm_clock_main_tile,None)
        self.activated_cont.set_width(lv.scr_act().get_disp().driver.hor_res)
        self.activated_cont.set_height(30)
        self.activated_cont.add_style(lv.label.PART.MAIN,alarm_clock_main_style)
        
        self.activated_label = lv.label(self.activated_cont,None)
        
        self.activated_label.align(self.activated_cont,lv.ALIGN.IN_LEFT_MID,10,0) # align left
        self.activated_label.set_text("Activated")
        self.activated_label.add_style(lv.label.PART.MAIN,alarm_clock_main_style)
        
        # create the activate switch      
        self.activated_switch = lv.switch(self.activated_cont,None)
        self.activated_switch.align(self.activated_cont,lv.ALIGN.IN_RIGHT_MID,-10,0)

        self.day_cont_style = lv.style_t()
        self.day_cont_style.copy(self.mainbar.get_style())
        self.day_cont_style.set_pad_inner(lv.STATE.DEFAULT,1)
        self.day_cont_style.set_pad_left(lv.STATE.DEFAULT,10)
        self.day_cont_style.set_pad_top(lv.STATE.DEFAULT,4)
        
        self.day_cont = lv.cont(alarm_clock_main_tile,None)
        self.day_cont.set_width(lv.scr_act().get_disp().driver.hor_res)
        self.day_cont.set_layout(lv.LAYOUT.PRETTY_BOTTOM)
        self.day_cont.set_fit(lv.FIT.NONE)
        self.day_cont.align(self.activated_cont,lv.ALIGN.OUT_BOTTOM_MID,0,0)
        self.day_cont.add_style(lv.cont.PART.MAIN,self.day_cont_style)
        
        # create the day buttons
        day_style = lv.style_t()
        day_style.set_radius(lv.STATE.DEFAULT, 3)

        for i in range(7):
            # create the button
            self.day_button[i] = lv.btn(self.day_cont,None)
            self.day_button[i].set_checkable(True)
            self.day_button[i].add_style(lv.btn.PART.MAIN,day_style)
            self.day_button[i].set_size(30,30)
            self.day_label[i] = lv.label(self.day_button[i])
            # print("Setting label %d text to: %s"%(i,self.weekDayTable_2[i]))
            self.day_label[i].set_text(self.alarm_clock_week_day_2[i])
            
        # create a roller for the hours
        for i in range(23):
            self.hours+=(str(i)+"\n")
        self.hours+=str(23)
        #print(self.hours)
        self.hourRoller = lv.roller(alarm_clock_main_tile,None)
        self.hourRoller.set_auto_fit(False)
        self.hourRoller.set_width(60)
        self.hourRoller.set_visible_row_count(4)
        self.hourRoller.set_options(self.hours,lv.roller.MODE.INFINITE)
        self.hourRoller.align(self.day_cont,lv.ALIGN.OUT_BOTTOM_LEFT,50,0)
        
        for i in range(59):
            # self.minutes += (str(i)+"\n")
            self.minutes += "%02d\n"%i
        self.minutes += str(59)
        self.minuteRoller = lv.roller(alarm_clock_main_tile,None)
        self.minuteRoller.set_auto_fit(False)
        self.minuteRoller.set_width(60)
        self.minuteRoller.set_visible_row_count(4)
        self.minuteRoller.set_options(self.minutes,lv.roller.MODE.INFINITE)
        self.minuteRoller.align(self.day_cont,lv.ALIGN.OUT_BOTTOM_RIGHT,-50,0)

        self.colon = lv.label(alarm_clock_main_tile,None)
        self.colon.set_text(":")
        self.colon.add_style(lv.label.PART.MAIN,self.day_cont_style)
        self.colon.align(self.hourRoller,lv.ALIGN.OUT_RIGHT_MID,0,0)

        exit_btn = lv.imgbtn(self.alarm_clock_main_tile,None)        
        exit_btn.set_src(lv.btn.STATE.RELEASED,self.mainbar.get_exit_btn_dsc())
        exit_btn.add_style(lv.imgbtn.PART.MAIN,alarm_clock_main_style)
        exit_btn.align(self.alarm_clock_main_tile,lv.ALIGN.IN_BOTTOM_LEFT, 10, -10 )
        self.log.debug("setting up exit callback")
        exit_btn.set_event_cb(self.exit_alarm_clock_main_event_cb)
        
        setup_btn = lv.imgbtn(self.alarm_clock_main_tile,None)
        setup_btn.set_src(lv.btn.STATE.RELEASED,self.mainbar.get_setup_btn_dsc())
        setup_btn.add_style(lv.imgbtn.PART.MAIN,alarm_clock_main_style)
        setup_btn.align(self.alarm_clock_main_tile,lv.ALIGN.IN_BOTTOM_RIGHT, -10, -10 )
        self.log.debug("setting up setup callback")
        # setup_btn.set_event_cb(self.alarm_clock_app_setup_event_cb)


    def enter_alarm_clock_main_event_cb(self,obj,evt):
        if evt == lv.EVENT.CLICKED:
            self.log.debug("enter_alarm_clock_app_event_cb called")
            self.statusbar.hide(True)
            # self.app.hide_indicator( example_app )
            self.mainbar.jump_to_tilenumber(self.main_tile_num, lv.ANIM.OFF )

    def exit_alarm_clock_main_event_cb(self,obj,evt):
        if evt == lv.EVENT.CLICKED:
            self.log.debug("exit_alarm_clock_app_event_cb called")
            self.statusbar.hide(False)
            self.mainbar.jump_to_maintile(lv.ANIM.OFF)
