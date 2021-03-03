#!/opt/bin/lv_micropython -i
import lvgl as lv
from lv_colors import lv_colors
from gui.icon import Icon

class ExampleApp():
    def __init__(self,mainbar):
        try:
            import ulogging as logging
        except:
            import logging
             
        self.log = logging.getLogger("ExampleApp")
        self.log.setLevel(logging.DEBUG)
        
        self.mainbar=mainbar
        self.statusbar=mainbar.gui.statusbar
        self.app = mainbar.app
        
        self.main_tile_num = mainbar.add_app_tile( 1, 2, "example app" )
        self.setup_tile_num = self.main_tile_num +1
        self.log.debug("tile number for main tile: %d",self.main_tile_num)
        self.example_app_main_tile = mainbar.get_tile_obj(self.main_tile_num)
        
        self.log.debug("registering example app")
        app=self.app.register("myapp","myapp_64px",self.enter_example_app_event_cb)
        self.app.set_indicator(app,Icon.INDICATOR_OK)
        self.main_page(self.main_tile_num)
        self.setup_page(self.setup_tile_num)
        
    def main_page(self,tile_num):
        example_app_main_tile = self.mainbar.get_tile_obj(tile_num);
        example_main_style = lv.style_t()
        example_main_style.copy(self.mainbar.get_style())
        
        exit_btn = lv.imgbtn(self.example_app_main_tile,None)        
        exit_btn.set_src(lv.btn.STATE.RELEASED,self.mainbar.get_exit_btn_dsc())
        exit_btn.add_style(lv.imgbtn.PART.MAIN,example_main_style)
        exit_btn.align(self.example_app_main_tile,lv.ALIGN.IN_BOTTOM_LEFT, 10, -10 )
        self.log.debug("setting up exit callback")
        exit_btn.set_event_cb(self.exit_example_app_main_event_cb)
        
        setup_btn = lv.imgbtn(self.example_app_main_tile,None)
        setup_btn.set_src(lv.btn.STATE.RELEASED,self.mainbar.get_setup_btn_dsc())
        setup_btn.add_style(lv.imgbtn.PART.MAIN,example_main_style)
        setup_btn.align(self.example_app_main_tile,lv.ALIGN.IN_BOTTOM_RIGHT, -10, -10 )
        self.log.debug("setting up setup callback")
        setup_btn.set_event_cb(self.enter_example_app_setup_event_cb)
        
        example_main_style.set_text_opa(lv.obj.PART.MAIN, lv.OPA._70)
        example_main_style.set_text_font(lv.STATE.DEFAULT,lv.font_montserrat_48)
        example_app_label = lv.label(self.example_app_main_tile,None)
        example_app_label.set_text("myapp")
        example_app_label.add_style(lv.obj.PART.MAIN,example_main_style)
        example_app_label.align(self.example_app_main_tile,lv.ALIGN.CENTER,0,0)
            
    def setup_page(self,tile_num):
        example_setup_tile = self.mainbar.get_tile_obj(tile_num)
        setup_style = lv.style_t()
        setup_style.copy(self.mainbar.get_style())
        setup_style.set_bg_color(lv.obj.PART.MAIN, lv_colors.GRAY)
        setup_style.set_bg_opa(lv.obj.PART.MAIN, lv.OPA.COVER)
        setup_style.set_border_width(lv.obj.PART.MAIN, 0)
        example_setup_tile.add_style(lv.obj.PART.MAIN, setup_style)

        exit_cont = lv.obj(example_setup_tile,None)
        exit_cont.set_size(lv.scr_act().get_disp().driver.hor_res,40)
        exit_cont.add_style(lv.obj.PART.MAIN, setup_style)

        exit_btn = lv.imgbtn(example_setup_tile,None)
        exit_btn.set_src(lv.btn.STATE.RELEASED,self.mainbar.get_exit_btn_dsc())
        exit_btn.set_src(lv.btn.STATE.PRESSED,self.mainbar.get_exit_btn_dsc())
        exit_btn.set_src(lv.btn.STATE.CHECKED_RELEASED,self.mainbar.get_exit_btn_dsc())
        exit_btn.set_src(lv.btn.STATE.CHECKED_PRESSED,self.mainbar.get_exit_btn_dsc())
        exit_btn.align(exit_cont,lv.ALIGN.IN_TOP_LEFT, 10, 0)
        exit_btn.set_event_cb(self.exit_example_app_setup_event_cb)

        exit_label = lv.label(exit_cont,None)
        exit_label.add_style(lv.obj.PART.MAIN, setup_style)
        exit_label.set_text("my app setup")
        exit_label.align(exit_btn, lv.ALIGN.OUT_RIGHT_MID, 5, 0 )

        foobar_switch_cont = lv.obj(example_setup_tile,None)
        foobar_switch_cont.set_size(lv.scr_act().get_disp().driver.hor_res,40)
        foobar_switch_cont.add_style(lv.obj.PART.MAIN, setup_style)
        foobar_switch_cont.align(exit_cont,lv.ALIGN.OUT_BOTTOM_LEFT, 0, 0 )

        foobar_switch = lv.switch(foobar_switch_cont,None)
        foobar_switch.add_protect(lv.PROTECT.CLICK_FOCUS)
        foobar_switch.add_style(lv.switch.PART.INDIC, setup_style)
        foobar_switch.off(lv.ANIM.ON)
        foobar_switch.align(foobar_switch_cont,lv.ALIGN.IN_RIGHT_MID, -5, 0 )
        self.log.debug("setting up the foobar switch callback")
        foobar_switch.set_event_cb(self.example_app_foobar_switch_event_cb)
        
        foobar_switch_label = lv.label(foobar_switch_cont,None)
        foobar_switch_label.add_style(lv.obj.PART.MAIN, setup_style)
        foobar_switch_label.set_text("foo bar")
        foobar_switch_label.align(foobar_switch_cont,lv.ALIGN.IN_LEFT_MID, 5, 0 )
        
    def enter_example_app_event_cb(self,obj,evt):
        if evt == lv.EVENT.CLICKED:
            self.log.debug("enter_app_event_cb called")
            self.statusbar.hide(True)
            # self.app.hide_indicator( example_app )
            self.mainbar.jump_to_tilenumber(self.main_tile_num, lv.ANIM.OFF )
            
    def exit_example_app_main_event_cb(self,obj,evt):
        if evt == lv.EVENT.CLICKED:
            self.log.debug("exit_app_event_cb called")
            self.statusbar.hide(False)
            self.mainbar.jump_to_maintile(lv.ANIM.OFF)
    
    def enter_example_app_setup_event_cb(self,obj,evt):
        if evt == lv.EVENT.CLICKED:
            self.log.debug("enter_example_app_setup-cb called")
            self.statusbar.hide(True)
            # self.app.hide_indicator( example_app )
            self.mainbar.jump_to_tilenumber(self.setup_tile_num, lv.ANIM.OFF )
            
    def exit_example_app_setup_event_cb(self,obj,evt):
        if evt == lv.EVENT.CLICKED:
            self.log.debug("exit_example_app_setup-cb called")
            self.mainbar.jump_to_tilenumber(self.main_tile_num,lv.ANIM.OFF)

    def example_app_foobar_switch_event_cb(self,obj,evt):
        if evt == lv.EVENT.VALUE_CHANGED:
            if obj.get_state():
                self.log.debug("switch value: on")
            else:
                self.log.debug("switch value: off")
