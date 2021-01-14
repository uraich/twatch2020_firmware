#!/opt/bin/lv_micropython -i
import lvgl as lv
from lv_colors import lv_colors
from micropython import const
try:
    import ulogging as logging
except:
    import logging
    
log = logging.getLogger("note_tile")
log.setLevel(logging.DEBUG)

class NoteTile():
    def __init__(self,parent):
        note_tile =  parent.add_tile( 0, 1, "note tile" )
        log.debug("Creating note tile")
        style = parent.get_style()
        note_style = lv.style_t()
        note_style.copy(style)
        note_style.set_text_opa(lv.obj.PART.MAIN, lv.OPA._30)
        note_style.set_text_font(lv.STATE.DEFAULT,lv.font_montserrat_48)
        
        note_label = lv.label(note_tile,None)
        note_label.set_text("note")
        note_label.add_style(lv.obj.PART.MAIN, note_style)
        note_label.align(None, lv.ALIGN.CENTER, 0, 0)
