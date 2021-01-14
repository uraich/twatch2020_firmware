#!/opt/bin/lv_micropython -i
import lvgl as lv
import time,sys
from display_driver_utils import driver
# Display a raw image

if len(sys.argv) != 4:
  print("Usage %s filename width height"%sys.argv[0])
  sys.exit()
filename = sys.argv[1]
width = int(sys.argv[2])
height = int(sys.argv[3])

drv = driver(width,height)

try:
  with open(filename,'rb') as f:
    img_data = f.read()
except:
  print("Could not open image file")
  sys.exit()
    
scr = lv.scr_act()
img = lv.img(scr)
img.align(scr, lv.ALIGN.CENTER, 0, 0)
img_dsc = lv.img_dsc_t(
    {
        "header": {"always_zero": 0, "w": width, "h": height, "cf": lv.img.CF.TRUE_COLOR_ALPHA},
        "data_size": len(img_data),
        "data": img_data,
    }
)

img.set_src(img_dsc)
img.set_x(0)
img.set_y(0)



