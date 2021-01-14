#!/opt/bin/lv_micropython -i
import lvgl as lv
from lv_colors import lv_colors
from micropython import const
try:
    import ulogging as logging
except:
    import logging

class App():
    def __init__(self,app_name, icon_dsc, event_cb):
        
