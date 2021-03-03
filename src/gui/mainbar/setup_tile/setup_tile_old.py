#!/opt/bin/lv_micropython -i
import lvgl as lv
from lv_colors import lv_colors
from micropython import const
try:
    import ulogging as logging
except:
    import logging

class SetupTile():    
    MAX_SETUP_ICON_HORZ =     3
    MAX_SETUP_ICON_VERT =     2
    MAX_SETUP_TILES     =     2
    MAX_SETUP_ICON      =     MAX_SETUP_ICON_HORZ * MAX_SETUP_ICON_VERT * MAX_SETUP_TILES

    setup_icon_files=['battery_icon_64px','brightness_64px','move_64px',
                      'wifi_64px','bluetooth_64px','time_64px',
                      'update_64px','utilities_64px','sound_64px']
    setup_names = ['battery','display', 'steps',
                   'wifi','bluetooth','time',
                   'update','utilities','sound']
    
    def __init__(self,mainbar):
        setup_cont = []
        log = logging.getLogger("Setup")
        log.setLevel(logging.DEBUG)
        self.SDL=0
        self.TWATCH=1
        y=1
        for tile_no in range(self.MAX_SETUP_TILES):
            id = "setup tile %s"%(tile_no+1)
            setup_cont.append(mainbar.add_tile(tile_no+1,y,id)) 

        self.style = lv.style_t()
        self.style.copy(mainbar.mainbar_style)
        
        self.setup_icon_data = [None]*self.MAX_SETUP_ICON
        self.setup_icon_dsc = [None]*self.MAX_SETUP_ICON
        self.setup_buttons=[None]*self.MAX_SETUP_ICON
        self.setup_labels=[None]*self.MAX_SETUP_ICON

        for i in range(len(self.setup_icon_files)):
            if i > self.MAX_SETUP_ICON:
                log.error("Too many setup programs")
                break;

            
            filename = self.setup_icon_files[i]
            try:
                sdl_filename = 'images/' + filename + "_argb8888.bin"
                log.debug('sdl filename: ' + sdl_filename)
                with open(sdl_filename,'rb') as f:
                    self.setup_icon_data[i] = f.read()
                    self.driver = self.SDL
                    log.debug(sdl_filename + " successfully read")
            except:
                twatch_filename = 'images/' + filename + "_argb565.bin"
                log.debug('t-watch filename: ' + twatch_filename)
                try:
                    with open(twatch_filename,'rb') as f:
                        self.setup_icon_data[i]= f.read()
                        self.driver = self.TWATCH
                        log.debug(twatch_filename + " successfully read")
                        
                except:
                    log.error("Could not find image file: " + filename) 
                    
            self.setup_icon_dsc[i] = lv.img_dsc_t(
                {
                    "header": {"always_zero": 0, "w": 64, "h": 64, "cf": lv.img.CF.TRUE_COLOR_ALPHA},
                    "data": self.setup_icon_data[i],
                    "data_size": len(self.setup_icon_data[i]),
                }
            )
            #
            # create the img buttons allowing to start the settings
            #
            x_pos = i%3 * 76 +12
            y_pos = (i-6*(i//6))//3 * 100 + 40
            print("x_pos: %d, y_pos: %d"%(x_pos,y_pos))

            self.setup_buttons[i] = lv.imgbtn(setup_cont[i//6],None)
            self.setup_buttons[i].set_src(lv.btn.STATE.RELEASED,self.setup_icon_dsc[i])
            self.setup_buttons[i].align(setup_cont[i//6],lv.ALIGN.IN_TOP_LEFT, x_pos, y_pos)

            self.setup_labels[i] = lv.label(setup_cont[i//6],None)
            self.setup_labels[i].set_text(self.setup_names[i])
            self.setup_labels[i].align(self.setup_buttons[i],lv.ALIGN.OUT_BOTTOM_MID,0,0)
