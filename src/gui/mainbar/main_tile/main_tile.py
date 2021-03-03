#!/opt/bin/lv_micropython -i
import lvgl as lv
import utime as time
from lv_colors import lv_colors
from micropython import const
from gui.icon import Icon
from gui.widget import MAX_WIDGET_NUM
from constants import Constants

try:
    import ulogging as logging
except:
    import logging
    


def dayOfWeekString(dayCode):
    weekDayTable= {
        0: "Mon",
        1: "Tue",
        2: "Wed",
        3: "Thu",
        4: "Fri",
        5: "Sat",
        6: "Sun",
        
    }
    return weekDayTable[dayCode]

def monthString (monthCode):
    monthTable= {
        1: "Jan",
        2: "Feb",
        3: "Mar",
        4: "Apr",
        5: "May",
        6: "Jun",
        7: "Jul",
        8: "Aug",
        9: "Sep",
        10: "Oct",
        11: "Nov",
        12: "Dec",
    }
    return monthTable[monthCode]


class MainTile():
    
    oldYear=-1
    oldMonth=-1
    oldDay=-1
    oldDate=[oldYear,oldMonth,oldDay]
    widget_table = [None] * MAX_WIDGET_NUM
    def __init__(self,mainbar):
        
        self.log = logging.getLogger("main_tile")
        self.log.setLevel(logging.DEBUG)

        self.log.debug("Creating main tile")
        self.mainbar = mainbar
        main_tile_no = mainbar.add_tile( 0, 0, "main tile" )
        main_tile = mainbar.get_tile_obj(main_tile_no)
        style = mainbar.get_style()
        

        self.clock_cont = lv.obj(main_tile,None)
        self.clock_cont.set_size(lv.scr_act().get_disp().driver.hor_res,
                                 lv.scr_act().get_disp().driver.ver_res//2)
        
        self.clock_cont.add_style(lv.obj.PART.MAIN,style)
        self.clock_cont.align(main_tile, lv.ALIGN.IN_TOP_MID, 0, 0)
        
        clocklabel_style = lv.style_t()
        clocklabel_style.set_text_font(lv.STATE.DEFAULT,lv.font_montserrat_48)

        self.clocklabel = lv.label(self.clock_cont,None)
        self.clocklabel.set_long_mode(lv.label.LONG.BREAK)  # Break the long lines
        self.clocklabel.set_recolor(True)                   # Enable re-coloring by commands in the text
        self.clocklabel.set_align(lv.label.ALIGN.LEFT)      # Center aligned lines
        self.clocklabel.set_text("#00ff00 11:35:00#")
        self.clocklabel.set_width(240)
        self.clocklabel.align(None,lv.ALIGN.OUT_TOP_MID, 30, 50)
        self.clocklabel.add_style(lv.label.PART.MAIN,clocklabel_style)

        self.datelabel = lv.label(self.clock_cont,None)
        self.datelabel.align(self.clocklabel,lv.ALIGN.OUT_BOTTOM_LEFT,40,20)
        self.datelabel.set_recolor(True)
        self.datelabel.set_text("#ffffff Mon 30.11.2020#")
        
        self.task = lv.task_create_basic()
        self.task.set_cb(lambda task: self.updateClock(task))
        self.task.set_period(1000)
        self.task.set_prio(lv.TASK_PRIO.MID)

        mainbar.main_tile = self
            
        #
        # init widgets
        #
        for i in range(MAX_WIDGET_NUM):
            self.widget_table[i] = Icon()
            self.widget_table[i].active = False
            self.widget_table[i].cont = mainbar.obj_create(main_tile)
            self.widget_table[i].cont.add_style(lv.obj.PART.MAIN,style)
            self.widget_table[i].cont.set_size(Constants.WIDGET_X_SIZE,Constants.WIDGET_Y_SIZE+20)
            # create app label
            self.widget_table[i].label = lv.label(self.widget_table[i].cont,None)
            mainbar.add_slide_element(self.widget_table[i].label)
            self.widget_table[i].label.add_style(lv.obj.PART.MAIN, style)
            self.widget_table[i].label.set_size(Constants.WIDGET_X_SIZE, Constants.WIDGET_LABEL_Y_SIZE)
            self.widget_table[i].label.set_align(lv.label.ALIGN.CENTER)
            self.widget_table[i].label.align(self.widget_table[i].cont,lv.ALIGN.IN_BOTTOM_LEFT, 0, -20 )
            # create app label
            self.widget_table[i].ext_label = lv.label(self.widget_table[i].cont,None)
            mainbar.add_slide_element(self.widget_table[i].ext_label)
            self.widget_table[i].ext_label.add_style(lv.obj.PART.MAIN,style)
            self.widget_table[i].ext_label.set_size(Constants.WIDGET_X_SIZE,Constants.WIDGET_LABEL_Y_SIZE)
            self.widget_table[i].ext_label.set_align(lv.label.ALIGN.CENTER)
            self.widget_table[i].ext_label.align(self.widget_table[i].label,lv.ALIGN.OUT_BOTTOM_LEFT, 0, 0)
            # create img and indicator
            self.widget_table[i].button_img = lv.imgbtn(self.widget_table[i].cont ,None)
            # self.widget_table[i].indicator = lv.img(self.widget_table[i].cont, None)

            # hide all
            self.widget_table[i].cont.set_hidden(True)
            self.widget_table[i].button_img.set_hidden(True)
            # self.widget_table[i].indicator.set_hidden(True)
            
            self.widget_table[i].label.set_hidden(True)
            self.widget_table[i].ext_label.set_hidden(True)
            
    def updateClock(self,task):
        # print(numericalClock.oldDate)
        if self.mainbar.pcf8563:
            # read time from pcf8563
            localTime = self.mainbar.pcf8563.datetime()
            year = localTime[0]+2000
        else:
            now = time.time()
            localTime = time.localtime(now)
            year = localTime[0]
            
        seconds = localTime[5]
        minutes = localTime[4]
        hours = localTime[3]
        month = localTime[1]
        day= localTime[2]
        weekday = localTime[6]
        # print('{}:{}:{}'.format(hours,minutes,seconds))
    
        timeText = '#00ff00 {:02d}:{:02d}:{:02d}#'.format(hours,minutes,seconds)
        # print(timeText)
        self.clocklabel.set_text(timeText)

        date = [year,month,day]
        if self.oldDate != date:
            dateText="#ffffff " + dayOfWeekString(weekday) + " " + str(day) + '.' + monthString(month) + ' ' + str(year) + "#"
            self.datelabel.set_text(dateText)
        self.oldDate = date
    
    def get_free_widget_icon(self):
        for i in range(MAX_WIDGET_NUM):
            if not self.widget_table[i].active:
                # print("widget number returned: %d",i)
                self.widget_table[i].active=True
                return self.widget_table[i]
        return None

    def align_widgets(self):
        active_widgets = 0
        xpos = 0
        for i in range(MAX_WIDGET_NUM):
            if self.widget_table[i].active:
                active_widgets += 1
        if active_widgets == 0:
            return
        xpos = 0 - ((Constants.WIDGET_X_SIZE*active_widgets)+((active_widgets-1)*Constants.WIDGET_X_CLEARENCE)) // 2
        # print("xpos: ",xpos)
        active_widgets = 0
        for i in range(MAX_WIDGET_NUM):
            if self.widget_table[i].active:
                self.widget_table[i].cont.align(self.clock_cont,lv.ALIGN.OUT_BOTTOM_MID,
                                                xpos + ( Constants.WIDGET_X_SIZE * active_widgets )
                                                + ( active_widgets * Constants.WIDGET_X_CLEARENCE ) + 32 , 20)
                active_widgets += 1


