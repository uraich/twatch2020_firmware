#!/opt/bin/lv_micropython -i
import lvgl as lv
from lv_colors import lv_colors
from micropython import const
from constants import Constants
try:
    import ulogging as logging
except:
    import logging

class ExampleApp():
    
    def __init__(self,parent,tile_num):
        self.tile = parent.get_tile_obj(tile_num)
        self.style = lv.style_t()
        self.style.copy(parent.mainbar_style)
        self.style.set_border_width(lv.obj.PART.MAIN, 0)
        self.tile.add_style( lv.obj.PART.MAIN, self.style)

        self.exit_cont = lv_obj( self.tile, None) 
        self.exit_cont.set_size( lv.scr_act().get_disp().driver.hor_res, 40)
        self.exit_cont.add_style(lv.obj.PART.MAIN, self.style )
        self.seit_cont.align(self.tile, lv.ALIGN.IN_TOP_MID, 0, 10)

        self.exit_btn = lv.imgbtn(self.exit_cont, None)
        '''
        lv_imgbtn_set_src( exit_btn, LV_BTN_STATE_RELEASED, &exit_32px);
    lv_imgbtn_set_src( exit_btn, LV_BTN_STATE_PRESSED, &exit_32px);
    lv_imgbtn_set_src( exit_btn, LV_BTN_STATE_CHECKED_RELEASED, &exit_32px);
    lv_imgbtn_set_src( exit_btn, LV_BTN_STATE_CHECKED_PRESSED, &exit_32px);
    lv_obj_add_style( exit_btn, LV_IMGBTN_PART_MAIN, &example_app_setup_style );
    lv_obj_align( exit_btn, exit_cont, LV_ALIGN_IN_TOP_LEFT, 10, 0 );
    lv_obj_set_event_cb( exit_btn, exit_example_app_setup_event_cb );
    
    lv_obj_t *exit_label = lv_label_create( exit_cont, NULL);
    lv_obj_add_style( exit_label, LV_OBJ_PART_MAIN, &example_app_setup_style  );
    lv_label_set_text( exit_label, "my app setup");
    lv_obj_align( exit_label, exit_btn, LV_ALIGN_OUT_RIGHT_MID, 5, 0 );
        '''
