#!/opt/bin/lv_micropython -i
import lvgl as lv
import utime as time
from lv_colors import lv_colors
from micropython import const
try:
    import ulogging as logging
except:
    import logging
    
log = logging.getLogger("main_tile")
log.setLevel(logging.DEBUG)

# Calculate the week day

def dayOfWeek(year,month,day):

    centuryCodeTable={
        1700: 4,
        1800: 2,
        1900: 0,
        2000: 6,
        2100: 4,
        2200: 2,
        2300: 0,
    }
    
    monthCodeTable = {
        1: 0,
        2: 3,
        3: 3,
        4: 6,
        5: 1,
        6: 4,
        7: 6,
        8: 2,
        9: 5,
        10: 0,
        11: 3,
        12: 5
    }
    
    y=year%100 # take only
    yearCode = y//4 + y
    yearCode %= 7

    # print("Year code: ",yearCode)

    century = year//100 * 100
    
    centuryCode =  centuryCodeTable[century]
    # print("Century Code: ",centuryCode)
    if year % 400 == 0:
        leapYearCode = 1
    elif year % 100 == 0:
        leapyearCode = 0
    elif year % 4 == 0:
        leapYearCode = 1
    else:
        leapYearCode = 0
        
    monthCode = monthCodeTable[month]
    dayCode = yearCode + monthCode + centuryCode +day
    # print("leapYearCode: ",leapYearCode)
    if month == 1 or month == 2:
        dayCode -= leapYearCode
        
    return dayCode % 7

def dayOfWeekString(dayCode):
    weekDayTable= {
        0: "Sun",
        1: "Mon",
        2: "Tue",
        3: "Wed",
        4: "Thu",
        5: "Fri",
        6: "Sat",
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
    
    def __init__(self,parent):
        log.debug("Creating main tile")
        main_tile = parent.add_tile( 0, 0, "main tile" )
        
        clocklabel_style = lv.style_t()
        clocklabel_style.set_text_font(lv.STATE.DEFAULT,lv.font_montserrat_48)
        
        self.clocklabel = lv.label(main_tile,None)
        self.clocklabel.set_long_mode(lv.label.LONG.BREAK)  # Break the long lines
        self.clocklabel.set_recolor(True)                   # Enable re-coloring by commands in the text
        self.clocklabel.set_align(lv.label.ALIGN.LEFT)      # Center aligned lines
        self.clocklabel.set_text("#00ff00 11:35:00#")
        self.clocklabel.set_width(240)
        self.clocklabel.align(None,lv.ALIGN.OUT_TOP_MID, 30, 50)
        self.clocklabel.add_style(lv.label.PART.MAIN,clocklabel_style)

        self.datelabel = lv.label(main_tile,None)
        self.datelabel.align(self.clocklabel,lv.ALIGN.OUT_BOTTOM_LEFT,40,20)
        self.datelabel.set_recolor(True)
        self.datelabel.set_text("#ffffff Mon 30.11.2020#")
        
        self.task = lv.task_create_basic()
        self.task.set_cb(lambda task: self.updateClock(task))
        self.task.set_period(1000)
        self.task.set_prio(lv.TASK_PRIO.LOWEST)

    def updateClock(self,task):
        # print(numericalClock.oldDate)
        try:
            localTime = cetTime()
        except:
            now = time.time()
            localTime = time.localtime(now)
        seconds = localTime[5]
        minutes = localTime[4]
        hours = localTime[3]
        year = localTime[0]
        month = localTime[1]
        day= localTime[2]

        # print('{}:{}:{}'.format(hours,minutes,seconds))
    
        timeText = '#00ff00 {:02d}:{:02d}:{:02d}#'.format(hours,minutes,seconds)
        # print(timeText)
        self.clocklabel.set_text(timeText)

        date = [year,month,day]
        if self.oldDate != date:
            weekday = dayOfWeek(year,month,day)
            dateText="#ffffff " + dayOfWeekString(weekday) + " " + str(day) + '.' + monthString(month) + ' ' + str(year) + "#"
            self.datelabel.set_text(dateText)
        self.oldDate = date
    
try:
    from wifi_connect import connect,cetTime
    # get time from the network
    connect()
except:
    pass
 
