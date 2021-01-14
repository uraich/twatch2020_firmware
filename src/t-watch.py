#!/opt/bin/lv_micropython -i
import lvgl as lv
from time import sleep
from display_driver_utils import driver
from lv_colors import lv_colors
try:
    import ulogging as logging
except:
    import logging
    
from gui.splashscreen import Splashscreen
from gui.gui import GUI

# log_level=["Trace", "Info", "Warning", "Error", "User"]
# lv.log_register_print_cb(lambda level,filename,line,func,msg:
                         # print('LOG: %s, file: %s in %s, line %d: %s' %
                               # (log_level[level], filename, func, line, msg)))

log = logging.getLogger("t-watch")
log.setLevel(logging.DEBUG)

class T_Watch():
    gui = None
    def __init__(self):
        drv = driver(width=240,height=240)

        scr_style = lv.style_t()
        scr_style.set_bg_color(lv.STATE.DEFAULT, lv_colors.BLACK)
        lv.scr_act().add_style(lv.obj.PART.MAIN,scr_style)
        
        log.debug("starting splash screen")
        splash = Splashscreen()
        sleep(2)
        splash.deinit()
        
        self.gui = GUI()
        
t_watch = T_Watch()

