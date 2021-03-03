#!/opt/bin/lv_micropython -i
import lvgl as lv
from time import sleep
from display_driver_utils import driver
from hardware.powermgr import PowerManager
from lv_colors import lv_colors
    
from gui.splashscreen import Splashscreen
from gui.gui import GUI

class T_Watch():
    gui = None
    drv = None
    def __init__(self):
        import ulogging as logging

        self.log = logging.getLogger("t-watch")
        self.log.setLevel(logging.DEBUG)            
        self.log.debug("Starting LVGL")
        self.drv = driver(width=240,height=240)

        scr_style = lv.style_t()
        scr_style.set_bg_color(lv.STATE.DEFAULT, lv_colors.BLACK)
        lv.scr_act().add_style(lv.obj.PART.MAIN,scr_style)
        
        self.log.debug("starting splash screen")
        splash = Splashscreen()
        sleep(1)
        splash.set_label("Starting WiFi")

        try:
            from hardware.wifi import WiFi
            wifi = WiFi()
            wifi.connect()
            #
            # get CET time from NTP and set up the pcf8563 RTC
            #
            self.pcf8563 = self.drv.watch.rtc        
            wifi.getTime()
            currentTime = wifi.cetTime()
            year = currentTime[0]
            month = currentTime[1]
            date = currentTime[2]
            hour = currentTime[3]
            minute = currentTime[4]
            second = currentTime[5]
            day = currentTime[6]            
            month_short = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
            day_of_week_short = ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]
            self.log.debug(" Setting RTC to %s %d. %s %02d %02d:%02d:%02d"%(day_of_week_short[day],
                                                                            date,month_short[month-1],year,
                                                                            hour,minute,second))
            self.pcf8563.set_datetime(currentTime)
        except:
            pass

        self.log.debug("Starting the power manager")
        if hasattr(self.drv,"watch"):
            print("Running on the twatch")
            self.powermgr = PowerManager(self.drv)        

        splash.deinit()
        self.gui = GUI(self.drv)

twatch = T_Watch()
