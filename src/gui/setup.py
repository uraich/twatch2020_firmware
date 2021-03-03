import lvgl as lv
from constants import Constants
from gui.app import App
from micropython import const
from lv_colors import lv_colors
from gui.icon import Icon
try:
    import ulogging as logging
except:
    import logging
    
class Setup():
    
    def __init__(self,mainbar):
        self.log = logging.getLogger("Setup")
        self.log.setLevel(logging.DEBUG)
        self.setup_icon_data = [None]*Constants.MAX_SETUP_ICON
        self.setup_icon_dsc = [None]*Constants.MAX_SETUP_ICON          
        self.mainbar = mainbar
        
    def setup_register(self,setup_name,icon_filename,event_cb):
        self.setup_tile = self.mainbar.gui.app_tile
        self.log.debug("register " + setup_name + " with icon filename " + icon_filename)
        setup = self.setup_tile.get_free_app_icon()
        if setup == None:
            return
        else:
            self.log.debug("Icon successfully registered")
            
        setup.active = True            # reserve the icon
        # setup label
        setup.label.set_text(setup_name)
        
        setup.label.align(setup.cont, lv.ALIGN.OUT_BOTTOM_MID, 0, 0 )
        setup.label.set_align(lv.label.ALIGN.CENTER );
        setup.cont.set_hidden(False)
        setup.label.set_hidden(False)
        #
        # setup icon and set event callback
        # create the img buttons allowing to start the apps
        #
        setup_style = lv.style_t()
        setup_style.copy(self.mainbar.get_style())
        #
        # create the imgbtn
        #
        setup.icon_img = lv.imgbtn(app.cont,None)
        
        (setup.icon_img_data,setup.icon_img_dsc) = self.get_setup_image(icon_filename)
        setup.icon_img.set_src(lv.btn.STATE.RELEASED,setup.icon_img_dsc)
        setup.icon_img.set_src(lv.btn.STATE.PRESSED,setup.icon_img_dsc)
        setup.icon_img.set_src(lv.btn.STATE.CHECKED_RELEASED,setup.icon_img_dsc)
        setup.icon_img.set_src(lv.btn.STATE.CHECKED_PRESSED,setup.icon_img_dsc)
        setup.icon_img.reset_style_list(lv.obj.PART.MAIN)
        setup.icon_img.align(setup.cont, lv.ALIGN.IN_TOP_LEFT, 0, 0 )
        setup.icon_img.set_event_cb(event_cb)
        self.log.debug("imgbtn position: %d,%d"%(setup.x,setup.y))        
        self.mainbar.add_slide_element( setup.icon_img )

        # setup the indicator
        setup.indicator = lv.img(setup.cont,None)
        setup.indicator.align(setup.cont, lv.ALIGN.IN_TOP_LEFT, 0, 0 )
        setup.indicator.set_hidden(True)
        
        lv.obj.invalidate( lv.scr_act() )
        return setup

    def get_setup_image(self,filename):

        try:
            sdl_filename = 'images/' + filename + "_argb8888.bin"
            self.log.debug('sdl filename: ' + sdl_filename)
            with open(sdl_filename,'rb') as f:
                setup_icon_data = f.read()
                self.log.debug(sdl_filename + " successfully read")
        except:
            twatch_filename = 'images/' + filename + "_argb565.bin"
            self.log.debug('t-watch filename: ' + twatch_filename)
            try:
                with open(twatch_filename,'rb') as f:
                    setup_icon_data = f.read()
                    self.log.debug(twatch_filename + " successfully read")
                    
            except:
                self.log.error("Could not find image file: " + filename) 

        setup_icon_dsc = lv.img_dsc_t(
            {
                "header": {"always_zero": 0, "w": 64, "h": 64, "cf": lv.img.CF.TRUE_COLOR_ALPHA},
                "data": setup_icon_data,
                "data_size": len(setup_icon_data),
            }
        )
        return (setup_icon_data,setup_icon_dsc) 
