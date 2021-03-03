import lvgl as lv
from lv_colors import lv_colors
from micropython import const
from gui.mainbar.setup_tile.battery_settings.battery_view import BatteryViewTile

try:
    import ulogging as logging
except:
    import logging

class BatterySettingsTile():
    
    def __init__(self,parent):
        self.log = logging.getLogger("battery settings")
        self.log.setLevel(logging.DEBUG)
        
        # get an app tile and copy mainstyle
    
        battery_settings_tile_num = parent.add_app_tile( 1, 2, "battery setup" )
        self.log.debug("Battery settings tile number: %d"%battery_settings_tile_num)
        battery_settings_tile = parent.get_tile_obj( battery_settings_tile_num + 1 );

        battery_settings_style = lv.style_t()
        battery_settings_style.copy(parent.get_style())

    def get_exit_icon(self):
        pass
        
        
                      
