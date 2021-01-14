#!/opt/bin/lv_micropython -i
# change the above to the path of your lv_micropython unix binary
#
import time
#
# initialize lvgl
#
import lvgl as lv
import display_driver
from info_2_8px_argb8888 import info_2_8px_img_dsc

# Create an object with the new style
obj = lv.img(lv.scr_act(), None)
lv.img.cache_set_size(2)

obj.set_src(info_2_8px_img_dsc)
obj.align(None, lv.ALIGN.CENTER, 0, 0)
