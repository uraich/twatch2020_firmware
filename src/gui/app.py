#!/opt/bin/lv_micropython -i
import lvgl as lv
from lv_colors import lv_colors
from constants import Constants
from micropython import const
from gui.icon import Icon

class App():
    def __init__(self,mainbar):
        try:
            import ulogging as logging
        except:
            import logging
        self.log = logging.getLogger("App")
        self.log.setLevel(logging.DEBUG)

        self.app_icon_data = [None]*Constants.MAX_APPS_ICON
        self.app_icon_dsc = [None]*Constants.MAX_APPS_ICON            

        self.indicator_icon_data = [None]*Icon.MAX_INDICATOR
        self.indicator_icon_dsc = [None]*Icon.MAX_INDICATOR
        self.indicator_filenames=["info_ok_16px","info_1_16px","info_2_16px","info_3_16px","info_n_16px",
                                  "info_fail_16px","info_update_16px"]                
        self.mainbar = mainbar
        # read all the indicator image files
        for i in range(Icon.MAX_INDICATOR):
            self.get_indicator_image(self.indicator_filenames[i],i)
        
        
    def register(self,app_name, icon_filename, event_cb):
        self.app_tile = self.mainbar.gui.app_tile
        self.log.debug("register " + app_name + " with icon filename " + icon_filename)
        app = self.app_tile.get_free_app_icon()
        if app == None:
            return
        else:
            self.log.debug("Icon successfully registered")
            
        app.active = True            # reserve the icon
        # setup label
        app.label.set_text(app_name)
        
        app.label.align(app.cont, lv.ALIGN.OUT_BOTTOM_MID, 0, 0 )
        app.label.set_align(lv.label.ALIGN.CENTER );
        app.cont.set_hidden(False)
        app.label.set_hidden(False)
        #
        # setup icon and set event callback
        # create the img buttons allowing to start the apps
        #
        app_style = lv.style_t()
        app_style.copy(self.mainbar.get_style())
        #
        # create the imgbtn
        #
        app.icon_img = lv.imgbtn(app.cont,None)
        
        (app.icon_img_data,app.icon_img_dsc) = self.get_app_image(icon_filename)
        app.icon_img.set_src(lv.btn.STATE.RELEASED,app.icon_img_dsc)
        app.icon_img.set_src(lv.btn.STATE.PRESSED,app.icon_img_dsc)
        app.icon_img.set_src(lv.btn.STATE.CHECKED_RELEASED,app.icon_img_dsc)
        app.icon_img.set_src(lv.btn.STATE.CHECKED_PRESSED,app.icon_img_dsc)
        app.icon_img.reset_style_list(lv.obj.PART.MAIN)
        app.icon_img.align(app.cont, lv.ALIGN.IN_TOP_LEFT, 0, 0 )
        app.icon_img.set_event_cb(event_cb)
        self.log.debug("imgbtn position: %d,%d"%(app.x,app.y))        
        self.mainbar.add_slide_element( app.icon_img )

        # setup the indicator
        app.indicator = lv.img(app.cont,None)
        app.indicator.align(app.cont, lv.ALIGN.IN_TOP_LEFT, 0, 0 )
        app.indicator.set_hidden(True)
        
        lv.obj.invalidate( lv.scr_act() )
        return app

    def set_indicator(self,app,indicator_type):
        if not app.active:
            return
        self.log.debug("set indicator %s"%self.indicator_filenames[indicator_type])
        app.indicator.set_src(self.indicator_icon_dsc[indicator_type])
        app.indicator.align(app.cont, lv.ALIGN.IN_TOP_RIGHT, 0, 0 )
        app.indicator.set_hidden(False)
        lv.obj.invalidate(lv.scr_act())
 
           
    def get_app_image(self,filename):

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
        
    def get_indicator_image(self,filename,indicator_type):

        try:
            sdl_filename = 'images/' + filename + "_argb8888.bin"
            self.log.debug('sdl filename: ' + sdl_filename)
            with open(sdl_filename,'rb') as f:
                self.indicator_icon_data[indicator_type] = f.read()
                self.log.debug(sdl_filename + " successfully read")
        except:
            twatch_filename = 'images/' + filename + "_argb565.bin"
            self.log.debug('t-watch filename: ' + twatch_filename)
            try:
                with open(twatch_filename,'rb') as f:
                    self.indicator_icon_data[indicator_type] = f.read()
                    self.log.debug(twatch_filename + " successfully read")
                    
            except:
                self.log.error("Could not find image file: " + filename) 

        self.indicator_icon_dsc[indicator_type] = lv.img_dsc_t(
            {
                "header": {"always_zero": 0, "w": 16, "h": 16, "cf": lv.img.CF.TRUE_COLOR_ALPHA},
                "data": self.indicator_icon_data[indicator_type],
                "data_size": len(self.indicator_icon_data[indicator_type]),
            }
        )

        return 
        
