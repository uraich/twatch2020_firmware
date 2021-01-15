#!/opt/bin/lv_micropython -i
import lvgl as lv
from lv_colors import lv_colors
from micropython import const
try:
    import ulogging as logging
except:
    import logging

class AppTile():    
    MAX_APPS_ICON_HORZ =     3
    MAX_APPS_ICON_VERT =     2
    MAX_APPS_TILES     =     2
    MAX_APPS_ICON      =     MAX_APPS_ICON_HORZ * MAX_APPS_ICON_VERT * MAX_APPS_TILES

    app_icon_files=['message_64px','weather_64px','mondaine_clock_64px',
                    'stopwatch_64px','alarm_clock_64px','calendar_64px',
                    'powermeter_64px','calculator_64px','status_64px']
    app_names = ['messages','weather\napp', 'analog\nclock',
                 'stop\nwatch','alarm clock','calendar',
                 'power\nmeter','calculator','status']
    
    def __init__(self,parent):
        tiles = []
        log = logging.getLogger("App")
        log.setLevel(logging.DEBUG)
        self.SDL=0
        self.TWATCH=1
        y=0
        for tile_no in range(self.MAX_APPS_TILES):
            id = "setup tile %s"%(tile_no+1)
            tiles.append(parent.add_tile(tile_no+1,y,id))
            
        self.app_icon_data = [None]*self.MAX_APPS_ICON
        self.app_icon_dsc = [None]*self.MAX_APPS_ICON
        self.app_buttons=[None]*self.MAX_APPS_ICON
        self.app_labels=[None]*self.MAX_APPS_ICON
        
        for i in range(len(self.app_icon_files)):
            if i > self.MAX_APPS_ICON:
                log.error("Too many apps")
                break
            
            filename = self.app_icon_files[i]
            try:
                sdl_filename = 'images/' + filename + "_argb8888.bin"
                log.debug('sdl filename: ' + sdl_filename)
                with open(sdl_filename,'rb') as f:
                    self.app_icon_data[i] = f.read()
                    self.driver = self.SDL
                    log.debug(sdl_filename + " successfully read")
            except:
                twatch_filename = 'images/' + filename + "_argb565.bin"
                log.debug('t-watch filename: ' + twatch_filename)
                try:
                    with open(twatch_filename,'rb') as f:
                        self.app_icon_data[i]= f.read()
                        self.driver = self.TWATCH
                        log.debug(twatch_filename + " successfully read")
                        
                except:
                    log.error("Could not find image file: " + filename) 
                    
            self.app_icon_dsc[i] = lv.img_dsc_t(
                {
                    "header": {"always_zero": 0, "w": 64, "h": 64, "cf": lv.img.CF.TRUE_COLOR_ALPHA},
                    "data": self.app_icon_data[i],
                    "data_size": len(self.app_icon_data[i]),
                }
            )
            #
            # create the img buttons allowing to start the apps
            #
            x_pos = i%3 * 76 +12
            y_pos = (i-6*(i//6))//3 * 100 + 40
            print("x_pos: %d, y_pos: %d"%(x_pos,y_pos))

            self.app_buttons[i] = lv.imgbtn(tiles[i//6],None)
            self.app_buttons[i].set_src(lv.btn.STATE.RELEASED,self.app_icon_dsc[i])
            self.app_buttons[i].align(tiles[i//6],lv.ALIGN.IN_TOP_LEFT, x_pos, y_pos)
            self.app_buttons[i].set_event_cb(self.exec_cb)
            
            self.app_labels[i] = lv.label(tiles[i//6],None)
            self.app_labels[i].set_text(self.app_names[i])
            self.app_labels[i].align(self.app_buttons[i],lv.ALIGN.OUT_BOTTOM_MID,0,0)

    def exec_cb(self,source,evt):
        for i in range(len(self.app_names)):
            if self.app_buttons[i] == source:
                print("Pressed: ",self.app_names[i])
