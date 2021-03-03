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
    
class SetupTile():
    
    def __init__(self,mainbar):
        self.setup_table = [None]*Constants.MAX_SETUP_ICON
        self.setup_tiles = []
        self.log = logging.getLogger("SetupTile")
        self.log.setLevel(logging.DEBUG)

        y = 1
        for tile_no in range(Constants.MAX_SETUP_TILES):
            id = "setup tile %s"%(tile_no+1)
            tile_num = mainbar.add_tile(tile_no+1,y,id)
            self.setup_tiles.append(mainbar.get_tile_obj(tile_num))

        self.style = lv.style_t()
        self.style.copy(mainbar.mainbar_style)

        #
        # create the setup_table
        #
        for i in range(Constants.MAX_SETUP_ICON):
            self.setup_table[i]=Icon()
            self.setup_table[i].active=False
            self.setup_table[i].x = Constants.SETUP_FIRST_X_POS+((i % Constants.MAX_SETUP_ICON_HORZ )
                                                                 * (Constants.SETUP_ICON_X_SIZE + Constants.SETUP_ICON_X_CLEARENCE))
            self.setup_table[i].y = Constants.SETUP_FIRST_Y_POS+(((i % (Constants.MAX_SETUP_ICON_VERT * Constants.MAX_SETUP_ICON_HORZ)) //
                                                                  Constants.MAX_SETUP_ICON_HORZ)*
                                                                 (Constants.SETUP_ICON_Y_SIZE + Constants.SETUP_ICON_Y_CLEARENCE))

            # create app icon container
            self.setup_table[i].cont = mainbar.obj_create( self.setup_tiles[ i // ( Constants.MAX_SETUP_ICON_HORZ * Constants.MAX_SETUP_ICON_VERT)])
            
            self.setup_table[i].cont.add_style(lv.obj.PART.MAIN,self.style )
            self.setup_table[i].cont.set_size(Constants.SETUP_ICON_X_SIZE, Constants.SETUP_ICON_Y_SIZE );
            self.setup_table[i].cont.align(self.setup_tiles[i // ( Constants.MAX_SETUP_ICON_HORZ * Constants.MAX_SETUP_ICON_VERT ) ],
                                           lv.ALIGN.IN_TOP_LEFT, self.setup_table[i].x, self.setup_table[i].y );

            # create app label
            self.setup_table[i].label= lv.label(self.setup_tiles[i//(Constants.MAX_SETUP_ICON_HORZ * Constants.MAX_SETUP_ICON_VERT)],None)
            mainbar.add_slide_element(self.setup_table[i].label);
            
            self.setup_table[i].label.add_style(lv.obj.PART.MAIN,self.style)
            self.setup_table[i].label.set_size(Constants.SETUP_LABEL_X_SIZE, Constants.SETUP_LABEL_Y_SIZE)
            self.setup_table[i].label.align( self.setup_table[i].cont, lv.ALIGN.OUT_BOTTOM_MID, 0, 0 )
            
            self.setup_table[i].cont.set_hidden(True)
            self.setup_table[i].label.set_hidden(True)
            
            self.log.debug("icon screen/x/y: %d/%d/%d"%(i // ( Constants.MAX_SETUP_ICON_HORZ * Constants.MAX_SETUP_ICON_VERT ),
                                                        self.setup_table[i].x, self.setup_table[i].y))

    def register_setup(self):
        for i in range(Constants.MAX_SETUP_ICON):
            if not self.setup_table[i].active:
                self.setup_table[i].active = True
                self.setup_table[i].cont.set_hidden(False)
                return self.setup_table[i]
        self.log.error("No space for new setup icon")
        return None

    def get_free_setup_icon(self):
        for i in range(Constants.MAX_SETUP_ICON):
            if not self.setup_table[i].active:
                self.setup_table[i].active = True
                return self.setup_table[i]
        self.log.error("No space for new setup icon")
        return None
