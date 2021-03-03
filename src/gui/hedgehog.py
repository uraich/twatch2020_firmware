#!/opt/bin/lv_micropython -i 
import lvgl as lv
import display_driver
from lv_colors import lv_colors
import time,sys

# Display a raw image
SDL     = 0
TWATCH = 1

scr_style = lv.style_t()
scr_style.set_bg_color(lv.STATE.DEFAULT, lv_colors.BLACK)
lv.scr_act().add_style(lv.obj.PART.MAIN,scr_style)

try:
  with open('images/hedgehog143x81_argb8888.bin','rb') as f:
    img_data = f.read()
    driver = SDL
except:
  try:
    with open('images/hedgehog143x81_rgb565.bin','rb') as f:
      img_data = f.read()
      driver = TWATCH
  except:
    print("Could not open hedgehog image file")
    sys.exit()
    
scr = lv.scr_act()
img = lv.img(scr)
img.align(scr, lv.ALIGN.CENTER, 0, 0)
if driver == SDL:
  img_dsc = lv.img_dsc_t(
    {
      "header": {"always_zero": 0, "w": 143, "h": 81, "cf": lv.img.CF.TRUE_COLOR_ALPHA},
      "data_size": len(img_data),
      "data": img_data,
    }
  )
else:
    img_dsc = lv.img_dsc_t(
    {
      "header": {"always_zero": 0, "w": 143, "h": 81, "cf": lv.img.CF.TRUE_COLOR},
      "data_size": len(img_data),
      "data": img_data,
    }
  )
img.set_src(img_dsc)
img.set_drag(False)


