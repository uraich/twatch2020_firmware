#!/opt/bin/lv_micropython -i
import lvgl as lv
from lv_colors import lv_colors
from micropython import const
from constants import Constants

class StatusBar():
    
    STATUSBAR_STYLE_NORMAL = const(0)
    STATUSBAR_STYLE_WHITE  = const(1)
    STATUSBAR_STYLE_RED    = const(2)
    STATUSBAR_STYLE_GRAY   = const(3)
    STATUSBAR_STYLE_YELLOW = const(4)
    STATUSBAR_STYLE_GREEN  = const(5)
    STATUSBAR_STYLE_BLUE   = const(6)
    STATUSBAR_STYLE_NUM    = const(7)


    def __init__(self,parent):
        try:
            import ulogging as logging
        except:
            import logging

        self.log = logging.getLogger("StatusBar")
        self.log.setLevel(logging.DEBUG)
        
        # read icons        
        sdl_filename = 'images/foot_16px_argb8888.bin'
        try:
            with open(sdl_filename,'rb') as f:
                self.foot_icon_data = f.read()
            self.log.debug(sdl_filename + " successfully read")
        except:
            twatch_filename = 'images/foot_16px_argb565.bin'
            try:
                with open(twatch_filename,'rb') as f:
                    self.foot_icon_data= f.read()
                    self.log.debug(twatch_filename + " successfully read")
            except:
                self.log.error("Could not find image file: 'images/foot_16px_argbxxx.bin") 
             

        self.foot_icon_dsc = lv.img_dsc_t(
            {
                "header": {"always_zero": 0, "w": 16, "h": 16, "cf": lv.img.CF.TRUE_COLOR_ALPHA},
                "data": self.foot_icon_data,
                "data_size": len(self.foot_icon_data),
            }
        )

        self.statusbar_style = [None]*self.STATUSBAR_STYLE_NUM
        
        self.statusbar_style[self.STATUSBAR_STYLE_NORMAL] = lv.style_t()
        self.statusbar_style[self.STATUSBAR_STYLE_NORMAL].init()
        self.statusbar_style[self.STATUSBAR_STYLE_NORMAL].set_radius(lv.obj.PART.MAIN, 0)
        self.statusbar_style[self.STATUSBAR_STYLE_NORMAL].set_bg_color(lv.obj.PART.MAIN,lv_colors.GREEN)
        self.statusbar_style[self.STATUSBAR_STYLE_NORMAL].set_bg_opa(lv.obj.PART.MAIN,lv.OPA._20)
        self.statusbar_style[self.STATUSBAR_STYLE_NORMAL].set_border_width(lv.obj.PART.MAIN,0)
        self.statusbar_style[self.STATUSBAR_STYLE_NORMAL].set_text_color(lv.obj.PART.MAIN,lv_colors.WHITE)
        self.statusbar_style[self.STATUSBAR_STYLE_NORMAL].set_image_recolor(lv.obj.PART.MAIN,lv_colors.WHITE)
         
        self.statusbar_style[self.STATUSBAR_STYLE_WHITE] = lv.style_t()
        self.statusbar_style[self.STATUSBAR_STYLE_WHITE].copy(self.statusbar_style[self.STATUSBAR_STYLE_NORMAL])
        self.statusbar_style[self.STATUSBAR_STYLE_WHITE].set_bg_opa(lv.obj.PART.MAIN,lv.OPA._0)
         
        self.statusbar_style[self.STATUSBAR_STYLE_RED] = lv.style_t()
        self.statusbar_style[self.STATUSBAR_STYLE_RED].copy(self.statusbar_style[self.STATUSBAR_STYLE_NORMAL])
        self.statusbar_style[self.STATUSBAR_STYLE_RED].set_bg_opa(lv.obj.PART.MAIN,lv.OPA._0)
        self.statusbar_style[self.STATUSBAR_STYLE_RED].set_text_color(lv.obj.PART.MAIN,lv_colors.RED)
        self.statusbar_style[self.STATUSBAR_STYLE_RED].set_image_recolor(lv.obj.PART.MAIN,lv_colors.RED)
         
        self.statusbar_style[self.STATUSBAR_STYLE_GRAY] = lv.style_t()
        self.statusbar_style[self.STATUSBAR_STYLE_GRAY].copy(self.statusbar_style[self.STATUSBAR_STYLE_NORMAL])
        self.statusbar_style[self.STATUSBAR_STYLE_GRAY].set_bg_opa(lv.obj.PART.MAIN,lv.OPA._0)
        self.statusbar_style[self.STATUSBAR_STYLE_GRAY].set_text_color(lv.obj.PART.MAIN,lv_colors.GRAY)
        self.statusbar_style[self.STATUSBAR_STYLE_GRAY].set_image_recolor(lv.obj.PART.MAIN,lv_colors.GRAY)

        self.statusbar_style[self.STATUSBAR_STYLE_YELLOW] = lv.style_t()
        self.statusbar_style[self.STATUSBAR_STYLE_YELLOW].copy(self.statusbar_style[self.STATUSBAR_STYLE_NORMAL])
        self.statusbar_style[self.STATUSBAR_STYLE_YELLOW].set_bg_opa(lv.obj.PART.MAIN,lv.OPA._0)
        self.statusbar_style[self.STATUSBAR_STYLE_YELLOW].set_text_color(lv.obj.PART.MAIN,lv_colors.YELLOW)
        self.statusbar_style[self.STATUSBAR_STYLE_YELLOW].set_image_recolor(lv.obj.PART.MAIN,lv_colors.YELLOW)

        self.statusbar_style[self.STATUSBAR_STYLE_GREEN] = lv.style_t()
        self.statusbar_style[self.STATUSBAR_STYLE_GREEN].copy(self.statusbar_style[self.STATUSBAR_STYLE_NORMAL])
        self.statusbar_style[self.STATUSBAR_STYLE_GREEN].set_bg_opa(lv.obj.PART.MAIN,lv.OPA._0)
        self.statusbar_style[self.STATUSBAR_STYLE_GREEN].set_text_color(lv.obj.PART.MAIN,lv_colors.GREEN)
        self.statusbar_style[self.STATUSBAR_STYLE_GREEN].set_image_recolor(lv.obj.PART.MAIN,lv_colors.GREEN)
         
        self.statusbar_style[self.STATUSBAR_STYLE_BLUE] = lv.style_t()
        self.statusbar_style[self.STATUSBAR_STYLE_BLUE].copy(self.statusbar_style[self.STATUSBAR_STYLE_NORMAL])
        self.statusbar_style[self.STATUSBAR_STYLE_BLUE].set_bg_opa(lv.obj.PART.MAIN,lv.OPA._0)
        self.statusbar_style[self.STATUSBAR_STYLE_BLUE].set_text_color(lv.obj.PART.MAIN,lv_colors.BLUE)
        self.statusbar_style[self.STATUSBAR_STYLE_BLUE].set_image_recolor(lv.obj.PART.MAIN,lv_colors.BLUE)
         
        self.status_bar = lv.cont(lv.scr_act())
        self.status_bar.set_width(lv.scr_act().get_disp().driver.hor_res)
        self.status_bar.set_height( Constants.STATUSBAR_HEIGHT )
        self.status_bar.reset_style_list( lv.obj.PART.MAIN )
        self.status_bar.add_style( lv.obj.PART.MAIN,self.statusbar_style[ self.STATUSBAR_STYLE_NORMAL ] )
        self.status_bar.align( lv.scr_act(), lv.ALIGN.IN_TOP_MID, 0, 0 )
       
        # self.status_bar.set_event_cb( statusbar_event )
        self.battery_label = lv.label(self.status_bar,None)
        self.battery_label.set_text('100%')
        self.battery_label.align(None,lv.ALIGN.IN_TOP_RIGHT,-5,4)
        
        self.battery_icon = lv.img(self.status_bar,None)
        self.battery_icon.set_src(lv.SYMBOL.BATTERY_FULL)
        self.battery_style = lv.style_t()
        self.battery_style.init()
        self.battery_style.copy(self.statusbar_style[self.STATUSBAR_STYLE_GREEN])        
        self.battery_style.set_image_recolor_opa(lv.obj.PART.MAIN,lv.OPA.COVER)
        self.battery_icon.align(self.battery_label,lv.ALIGN.OUT_LEFT_MID, -5, 0)
        self.battery_icon.add_style(lv.obj.PART.MAIN,self.battery_style)
        
        self.wifi_icon = lv.img(self.status_bar,None)
        self.wifi_icon.set_src(lv.SYMBOL.WIFI)
        self.wifi_icon.align(self.battery_icon,lv.ALIGN.OUT_LEFT_MID, -5, 0)

        self.step_icon = lv.img(self.status_bar,None)
        self.step_icon.set_src(self.foot_icon_dsc)
        self.step_icon.align(self.status_bar,lv.ALIGN.IN_TOP_LEFT, 5, 4)

        self.step_counter = lv.label(self.status_bar,None)
        self.step_counter.set_text('0')
        self.step_counter.align(self.step_icon,lv.ALIGN.OUT_RIGHT_MID, 3, 0)

    def hide(self,hide):
        self.status_bar.set_hidden(hide)
