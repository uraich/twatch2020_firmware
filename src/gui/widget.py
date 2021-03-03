#!/opt/bin/lv_micropython -i
import lvgl as lv
from lv_colors import lv_colors
from constants import Constants
from micropython import const

MAX_WIDGET_NUM = 3

class Widget():
    def __init__(self,mainbar):
        try:
            import ulogging as logging
        except:
            import logging
        self.log = logging.getLogger("App")
        
        self.log.setLevel(logging.DEBUG)
        self.mainbar = mainbar
        self.main_tile = mainbar.main_tile
        
    def register(self,widget_name, icon, event_cb):
        widget = self.main_tile.get_free_widget_icon()
        if not widget:
            self.log.error("no free widget icon")
            return None
        wn=widget_name.replace(" ","\n")
        widget.label.set_text(wn)
        widget.button_img.set_src(lv.btn.STATE.RELEASED,icon)
        widget.button_img.set_src(lv.btn.STATE.RELEASED,icon)
        widget.button_img.set_src(lv.btn.STATE.RELEASED,icon)
        widget.button_img.set_src(lv.btn.STATE.RELEASED,icon)
        widget.button_img.set_event_cb(event_cb)
        # make everything visible
        widget.button_img.set_hidden(False)
        widget.label.set_hidden(False)
        # widget.ext_label.set_hidden(False)
        widget.cont.set_hidden(False)
        # widget.indicator.set_hidden(False)

        self.mainbar.add_slide_element(widget.cont)
        self.mainbar.add_slide_element(widget.button_img)
        self.main_tile.align_widgets()
        lv.scr_act().invalidate()
        return widget
        
        
