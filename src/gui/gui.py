#!/opt/bin/lv_micropython -i
import lvgl as lv
from lv_colors import lv_colors
from micropython import const
from gui.statusbar import StatusBar
from gui.mainbar.mainbar import MainBar
from gui.mainbar.main_tile.main_tile import MainTile
from gui.mainbar.app_tile.app_tile import AppTile
from gui.mainbar.note_tile.note_tile import NoteTile
from gui.mainbar.setup_tile.setup_tile import SetupTile
from gui.mainbar.setup_tile.battery_settings.battery_settings import BatterySettingsTile

try:
    import ulogging as logging
except:
    import logging

class GUI():
    mainbar = None
    main_tile = None
    app_tile = None
    note_tile = None
    setup_tile = None
    status_bar = None
    battery_settings_tile = None
    wallpaper_images = ["bg_240px","bg1_240px","bg2_240px","bg3_240px"]
    def __init__(self):
        self.log = logging.getLogger("gui")
        self.log.setLevel(logging.DEBUG)
                          
        # create wallpaper
        self.wallpaper = lv.img(lv.scr_act(),None)
        self.wallpaper.set_width(lv.scr_act().get_disp().driver.hor_res)
        self.wallpaper.set_height(lv.scr_act().get_disp().driver.ver_res)
        self.set_background_image(self.wallpaper_images[2])
        self.wallpaper.align(None, lv.ALIGN.CENTER, 0, 0)
        
        self.statusbar = StatusBar(self.mainbar)

        self.mainbar = MainBar(lv.scr_act())

        # add the four mainbar screens
        self.main_tile = MainTile(self.mainbar)
        self.log.debug("Creating app tile")                          
        self.app_tile = AppTile(self.mainbar)
        self.log.debug("Creating Note tile")
        self.note_tile = NoteTile(self.mainbar)
        self.log.debug("Creating Setup tile")
        self.setup_tile = SetupTile(self.mainbar)
        
        # add setup
        battery_settings_tile = BatterySettingsTile(self.mainbar)

    def set_background_image(self,image_filename):
        SDL=0
        TWATCH=1
        self.sdl_filename = image_filename + "_argb8888.bin"
        self.twatch_filename = image_filename + "_rgb565.bin"
        self.log.debug("sdl filename: " + "images/" + self.sdl_filename)
        self.log.debug("t-watch filename: "+ "images/" + self.twatch_filename)
        try:
            with open('images/'+self.sdl_filename,'rb') as f:
                img_data = f.read()
                self.log.debug(self.sdl_filename + " successfully read")
                driver = SDL
        except:
            try:
                with open('/images/'+self.twatch_filename,'rb') as f:
                    img_data = f.read()
                    self.log.debug(self.twatch_filename + " successfully read")
                    driver = TWATCH
            except:
                self.log.error("Could not open " + image_filename)
                self.wallpaper.set_hidden(True)
                return

        if driver == SDL:
            self.img_dsc = lv.img_dsc_t(
                {
                    "header": {"always_zero": 0, "w": 240, "h": 240,
                               "cf": lv.img.CF.TRUE_COLOR_ALPHA},
                    "data_size": len(img_data),
                    "data": img_data,
                }
            )
        else:
            self.img_dsc = lv.img_dsc_t(
                {
                    "header": {"always_zero": 0, "w": 240, "h": 240,
                               "cf": lv.img.CF.TRUE_COLOR},
                    "data_size": len(img_data),
                    "data": img_data,
                }
            )
            
        self.wallpaper.set_src(self.img_dsc)
        self.wallpaper.align(None, lv.ALIGN.CENTER, 0, 0 )
        self.wallpaper.set_hidden(False)
