# place holder for an application
class Icon():    
    INDICATOR_OK     = 0
    INDICATOR_1      = 1
    INDICATOR_2      = 2
    INDICATOR_3      = 3
    INDICATOR_N      = 4
    INDICATOR_FAIL   = 5
    INDICATOR_UPDATE = 6
    MAX_INDICATOR    = INDICATOR_UPDATE +1

    BTN_SETUP   = 0
    BTN_REFRESH = 1
    BTN_EXIT    = 2
    
    def __init__(self):
        self.cont = None
        self.button_img_data = None
        self.button_img_dsc = None
        self.button_img = None
        self.indicator = None
        self.label = None
        self.ext_label = None
        self.event_cb = None
        self.x=0
        self.y=0
        self.active = False
