from micropython import const
class Constants:
    MAINBAR_APP_TILE_X_START = const(0)
    MAINBAR_APP_TILE_Y_START = const(4)
    STATUSBAR_HEIGHT = const(26)
    STATUS_BAR_WIDTH = const(200)
    
    MAX_APPS_ICON_HORZ = 3
    MAX_APPS_ICON_VERT = 2
    MAX_APPS_TILES     = 3
    MAX_APPS_ICON = MAX_APPS_ICON_HORZ * MAX_APPS_ICON_VERT * MAX_APPS_TILES

    APP_ICON_X_SIZE = 64
    APP_ICON_Y_SIZE = 64
    APP_ICON_X_CLEARENCE = 8
    APP_ICON_Y_CLEARENCE = 36

    APP_LABEL_X_SIZE = APP_ICON_X_SIZE + APP_ICON_X_CLEARENCE
    APP_LABEL_Y_SIZE = APP_ICON_Y_CLEARENCE // 2
    
    APP_FIRST_X_POS = (240-(APP_ICON_X_SIZE*MAX_APPS_ICON_HORZ+APP_ICON_X_CLEARENCE*(MAX_APPS_ICON_HORZ-1))) // 2
    APP_FIRST_Y_POS = (240-(APP_ICON_Y_SIZE*MAX_APPS_ICON_VERT+APP_ICON_Y_CLEARENCE*(MAX_APPS_ICON_VERT-1))) // 2

    WIDGET_X_SIZE = 64
    WIDGET_Y_SIZE = 80
    WIDGET_X_CLEARENCE = 16
    WIDGET_LABEL_Y_SIZE = 16

    MAX_SETUP_ICON_HORZ =       3
    MAX_SETUP_ICON_VERT =       2
    MAX_SETUP_TILES     =       2
    MAX_SETUP_ICON      =  MAX_SETUP_ICON_HORZ * MAX_SETUP_ICON_VERT * MAX_SETUP_TILES
    
    SETUP_ICON_X_SIZE =        64
    SETUP_ICON_Y_SIZE =        64
    SETUP_ICON_X_CLEARENCE =    8
    SETUP_ICON_Y_CLEARENCE =   36
    SETUP_LABEL_X_SIZE     =   SETUP_ICON_X_SIZE + SETUP_ICON_X_CLEARENCE
    SETUP_LABEL_Y_SIZE     =   SETUP_ICON_Y_CLEARENCE // 2

    SETUP_FIRST_X_POS =  ( 240 - ( SETUP_ICON_X_SIZE * MAX_SETUP_ICON_HORZ + SETUP_ICON_X_CLEARENCE * ( MAX_SETUP_ICON_HORZ - 1 ) ) ) // 2
    SETUP_FIRST_Y_POS =  ( 240 - ( SETUP_ICON_Y_SIZE * MAX_SETUP_ICON_VERT + SETUP_ICON_Y_CLEARENCE * ( MAX_SETUP_ICON_VERT - 1 ) ) ) // 2
