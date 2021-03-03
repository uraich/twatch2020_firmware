import lvgl as lv
from lv_colors import lv_colors
try:
    import ulogging as logging
except:
    import logging

import sys
class Splashscreen():
    def __init__(self):
        # create a logger
        self.log = logging.getLogger("Splashscreen")
        self.log.setLevel(logging.DEBUG)
        
        scr_style = lv.style_t()
        scr_style.set_bg_color(lv.STATE.DEFAULT, lv_colors.BLACK)
        lv.scr_act().add_style(lv.obj.PART.MAIN,scr_style)
        
        try:
            with open('images/hedgehog143x81_argb8888.bin','rb') as f:
                hedgehog_data = f.read()
                self.log.debug("hedgehog143x81_argb8888.bin successfully read")
        except:
            try:
                with open('images/hedgehog143x81_argb565.bin','rb') as f:
                    hedgehog_data = f.read()
                    self.log.debug("hedgehog143x81_argb565.bin successfully read")
            except:
                self.log.error("Could not open hedgehog image file")
                sys.exit()

    
        self.image = lv.img(lv.scr_act(),None)

        img_dsc = lv.img_dsc_t(
            {
                "header": {"always_zero": 0, "w": 143, "h": 81,
                           "cf": lv.img.CF.TRUE_COLOR_ALPHA},
                "data_size": len(hedgehog_data),
                "data": hedgehog_data,
            }
        )

        self.image.set_src(img_dsc)
        self.image.align(None,lv.ALIGN.CENTER,0,-20)
        
        self.text_style = lv.style_t()
        self.text_style.init()
        self.text_style.set_text_color(lv.STATE.DEFAULT,lv_colors.WHITE)
        self.label = lv.label(lv.scr_act(),None)
        self.label.add_style(lv.label.PART.MAIN,self.text_style)
        self.label.set_text("Starting up...")
        self.label.align(self.image,lv.ALIGN.IN_BOTTOM_MID,0,50)
        

    def set_label(self,text):
        self.label.set_text(text)
        
    def deinit(self):
        self.image.delete()
        self.label.delete()
