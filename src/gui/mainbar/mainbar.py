import lvgl as lv
from constants import Constants
from micropython import const
from lv_colors import lv_colors
try:
    import ulogging as logging
except:
    import logging
    
class MainBar():
    
    tile_table = []
    current_tile = 0
    tile_entries = 0
    app_tile_pos = Constants.MAINBAR_APP_TILE_X_START
    
    TILE = const(0)
    HIBERNATE_CB = const(1)
    ACTIVATE_CB  = const(2)
    TILE_X = const(3)
    TILE_Y = const(4)
    TILE_ID = const(5)

    exit_icon_dsc = None
    setup_icon_dsc = None
    
    def __init__(self,parent):
        
        self.log = logging.getLogger("mainbar")
        self.log.setLevel(logging.DEBUG)
        
        self.mainbar_style=lv.style_t()
        self.mainbar_style.init()
        self.mainbar_style.set_radius(lv.obj.PART.MAIN, 0 )
        self.mainbar_style.set_bg_color(lv.obj.PART.MAIN,lv_colors.GRAY)
        self.mainbar_style.set_bg_opa(lv.obj.PART.MAIN,lv.OPA._0 )
        
        self.mainbar_style.set_border_width(lv.obj.PART.MAIN,0)
        self.mainbar_style.set_text_color(lv.obj.PART.MAIN,lv_colors.WHITE)
        self.mainbar_style.set_image_recolor(lv.obj.PART.MAIN,lv_colors.WHITE)

        self.mainbar_switch_style = lv.style_t()
        self.mainbar_switch_style.init()
        self.mainbar_switch_style.set_bg_color(lv.STATE.CHECKED,lv_colors.GREEN)

        self.mainbar_slider_style = lv.style_t()
        self.mainbar_slider_style.init()
        self.mainbar_slider_style.set_bg_color(lv.STATE.DEFAULT,lv_colors.GREEN)

        self.mainbar_button_style = lv.style_t()
        self.mainbar_button_style.init()
        self.mainbar_button_style.set_radius(lv.STATE.DEFAULT, 3 )
        self.mainbar_button_style.set_border_color(lv.STATE.DEFAULT,lv_colors.WHITE)
        self.mainbar_button_style.set_border_opa(lv.STATE.DEFAULT,lv.OPA._70 )
        self.mainbar_button_style.set_border_width(lv.STATE.DEFAULT,2)

        self.mainbar = lv.tileview(parent, None)
        self.mainbar.set_edge_flash(False)
        self.mainbar.add_style(lv.obj.PART.MAIN,self.mainbar_style)
        lv.page.set_scrollbar_mode( lv.page.__cast__(self.mainbar), lv.SCROLLBAR_MODE.OFF)

        self.exit_icon_dsc = self.get_image_dsc('exit_32px')
        self.setup_icon_dsc = self.get_image_dsc('setup_32px')


    def get_style(self):
        return self.mainbar_style
    
    def get_switch_style(self):
        return(self.switch_style)

    def get_button_style(self):
        return(self.switch_style)
    
    def get_slider_style(self):
        return(self.slider_style)
    
    def add_tile(self,x,y,id):
        
        self.tile_entries +=1
        
        tile = lv.cont(self.mainbar,None)
        hor_res = lv.scr_act().get_disp().driver.hor_res
        ver_res = lv.scr_act().get_disp().driver.ver_res
        tile.set_width(hor_res)
        tile.set_height(ver_res)
        tile.set_pos(hor_res*x,ver_res*y)   
        tile.add_style(lv.obj.PART.MAIN, self.mainbar_style)
        tile_table_entry = (tile,None,None,x,y,id)
        self.tile_table.append(tile_table_entry)
        self.mainbar.add_element(tile)
        valid_pos = []
        for i in range(len(self.tile_table)):
            valid_pos.append({'x':self.tile_table[i][3],'y':self.tile_table[i][4]})
        
        self.mainbar.set_valid_positions(valid_pos,len(valid_pos))
      
        self.log.debug("add tileno %d: x: %d, y: %d, id: %s"%(self.tile_entries,
                                                              tile_table_entry[self.TILE_X],
                                                              tile_table_entry[self.TILE_Y],
                                                              tile_table_entry[self.TILE_ID]))
        return tile

    def add_tile_hibernate_cb(self,tile_number,hibernate_cb):
        if tile_number < self.tile_entries:
            tile[tile_number][self.HIBERNATE_CB] = hibernate_cb
        else:
            self.log.error("tile number %d does not exist"%tile_number)
                  
    def add_tile_activate_cb(self,tile_number,activate_cb):
        if tile_number < self.tile_entries:
            tile[tile_number][self.HIBERNATE_CB] = activate_cb
        else:
            self.log.error("tile number %d does not exist"%tile_number)

    def add_app_tile(self,x,y,id):
        tile_no = self.tile_entries+1 
        for hor in range(x):
            for ver in range(y):
                self.add_tile( hor + self.app_tile_pos, ver + Constants.MAINBAR_APP_TILE_Y_START, id )        
        return tile_no

    def get_tile_obj(self,tile_number):
        if tile_number < self.tile_entries:
            return self.tile_table[tile_number][TILE]

    def jump_to_tilenumber(self,tile_num,anim):
        if tile_num < self.tile_entries:
            self.log.debug("jump to tile %d from tile %d"%(tile_num,self.current_tile))
            self.mainbar._set_tile_act(self.tile_table[tile_num][TILE_X],
                                       self.tile_table[tile_num][TILE_Y])
            # call hibernate_cb if callback exists
            if self.tile_table[self.current_tile][HIBERNATE_CB]:
                self.log.debug("call hibernate cb for tile: %d"%self.current_tile)
                self.tile_table[self.current_tile][HIBERNATE_CB]
                
            # call activate_cb for new tile if callback exists
            if self.tile_table[self.tile_num][ACTIVATE_CB]:
                self.log.debug("call activate cb for tile %d"%tile_num)
                self.tile_table[self.current_tile][ACTIVATE_CB]
            self.current_tile = tile_num
        else:
            self.log.error("tile number: %d does not exist"%tile_num)

    def get_exit_btn_dsc(self):
        return self.exit_icon_dsc

    def get_setup_dsc(self):
        return self.setup_icon_dsc

    def get_image_dsc(self,filename):
        
        self.log.debug("Creating " + filename + " icon") 
        try:
            sdl_filename = 'images/' + filename + "_argb8888.bin"
            self.log.debug('sdl filename: ' + sdl_filename)
            with open(sdl_filename,'rb') as f:
                self.icon_data = f.read()
                self.log.debug(sdl_filename + " successfully read")
        except:
            twatch_filename = 'images/' + filename + "_argb565.bin"
            self.log.debug('t-watch filename: ' + twatch_filename)
            try:
                with open(twatch_filename,'rb') as f:
                    self.icon_data = f.read()
                    self.log.debug(twatch_filename + " successfully read")
                    
            except:
                self.log.error("Could not find image file: " + filename) 

        self.icon_dsc = lv.img_dsc_t(
            {
                "header": {"always_zero": 0, "w": 32, "h": 32, "cf": lv.img.CF.TRUE_COLOR_ALPHA},
                "data": self.icon_data,
                "data_size": len(self.icon_data),
            }
        )
        return self.icon_dsc
