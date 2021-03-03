import lvgl as lv
import cmath
from lv_colors import lv_colors
from gui.icon import Icon
import utime as time

# Line defined by polar coords; origin and line are complex
def polar(canvas, origin, line, width, color):
    line_dsc = lv.draw_line_dsc_t()
    line_dsc.init()
    line_dsc.color = color
    line_dsc.width = width
    p1=lv.point_t()
    p2=lv.point_t()    
    point_array=[p1,p2]
    
    xs, ys = origin.real, origin.imag
    p1.x=round(xs)
    p1.y=round(ys)
    p2.x=round(xs + line.real)
    p2.y=round(ys - line.imag)
    # print("x0: %d, y0: %d, x1: %d, y1: %d"%(round(xs), round(ys), round(xs + line.real), round(ys - line.imag)))
    canvas.draw_line(point_array, 2, line_dsc)

def conj(v):  # complex conjugate
    return v.real - v.imag * 1j


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

class AnalogueClock():
    oldYear=-1
    oldMonth=-1
    oldDay=-1
    oldHour=-1
    oldMin=-1
    oldSec=-1
    oldDate=[oldYear,oldMonth,oldDay]
    
    def __init__(self,mainbar):
        try:
            import ulogging as logging
        except:
            import logging
             
        self.log = logging.getLogger("AnalogueClockApp")
        self.log.setLevel(logging.DEBUG)
        
        self.mainbar=mainbar
        self.statusbar=mainbar.gui.statusbar
        self.app = mainbar.app
        
        self.tile_num = mainbar.add_app_tile( 1, 1, "analogue clock app" )
        self.log.debug("tile number for main tile: %d",self.tile_num)
        
        self.log.debug("registering analogue clock app")
        app=self.app.register("analogue\nclock","mondaine_clock_64px",self.enter_aclock_app_event_cb)
        self.main_page(self.tile_num)
        
    def main_page(self,tile_num):
        self.aclock_tile = self.mainbar.get_tile_obj(tile_num);
        self.aclock_style = lv.style_t()
        self.aclock_style.copy(self.mainbar.get_style())
        
        self.CANVAS_HEIGHT = lv.scr_act().get_disp().driver.ver_res
        self.CANVAS_WIDTH = self.CANVAS_HEIGHT
        cbuf=bytearray(self.CANVAS_HEIGHT * self.CANVAS_HEIGHT * 4)

        self.canvas = lv.canvas(self.aclock_tile,None)
        self.canvas.set_buffer(cbuf,self.CANVAS_HEIGHT,self.CANVAS_HEIGHT,lv.img.CF.TRUE_COLOR)
        self.canvas.align(self.aclock_tile,lv.ALIGN.CENTER,0,0)
        
        circle_dsc = lv.draw_line_dsc_t()
        circle_dsc.init()
        circle_dsc.color = lv_colors.GREEN
        self.radius = 90
        xo=self.CANVAS_WIDTH//2
        yo=self.CANVAS_HEIGHT//2-20
        self.canvas.draw_arc(xo,yo,self.radius,0,360,circle_dsc)
        vor = xo + 1j * yo
        vtstart = 0.9 * self.radius + 0j  # start of tick
        vtick = 0.1 * self.radius + 0j  # tick
        vrot = cmath.exp(2j * cmath.pi/12)  # unit rotation
        for _ in range(12):
            polar(self.canvas, vor + conj(vtstart), vtick, 1, lv_colors.GREEN)
            vtick *= vrot
            vtstart *= vrot
            
        vtick = 0.05 * self.radius + 0j  # tick
        vrot = cmath.exp(2j * cmath.pi/60)  # unit rotation
        for _ in range(60):
            polar(self.canvas, vor + conj(vtstart), vtick, 1, lv_colors.GREEN)
            vtick *= vrot
            vtstart *= vrot
            self.hrs_radius = self.radius-32
            self.min_radius = self.radius -12
            self.sec_radius = self.radius -12

        self.task = lv.task_create_basic()
        self.task.set_cb(lambda task: self.updateClock(self.task))
        self.task.set_period(100)
        self.task.set_prio(lv.TASK_PRIO.LOWEST)

        exit_btn = lv.imgbtn(self.aclock_tile,None)        
        exit_btn.set_src(lv.btn.STATE.RELEASED,self.mainbar.get_exit_btn_dsc())
        exit_btn.add_style(lv.imgbtn.PART.MAIN,self.aclock_style)
        exit_btn.align(self.aclock_tile,lv.ALIGN.IN_BOTTOM_LEFT, 10, -10 )
        self.log.debug("setting up exit callback")
        exit_btn.set_event_cb(self.exit_aclock_app_event_cb)
        
        self.aclock_style.set_text_opa(lv.obj.PART.MAIN, lv.OPA.COVER)
            
    def enter_aclock_app_event_cb(self,obj,evt):
        if evt == lv.EVENT.CLICKED:
            self.log.debug("enter_aclock_app_event_cb called")
            self.statusbar.hide(True)
            # self.app.hide_indicator( example_app )
            self.mainbar.jump_to_tilenumber(self.tile_num, lv.ANIM.OFF )
            
    def exit_aclock_app_event_cb(self,obj,evt):
        if evt == lv.EVENT.CLICKED:
            self.log.debug("exit_aclock_app_event_cb called")
            self.statusbar.hide(False)
            self.mainbar.jump_to_maintile(lv.ANIM.OFF)
    
    def updateClock(self,task):
        center=120+100j
        
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
    
        if hours > 12:
            hours -= 12
        hours *=5             # the angle corresponding to the hour 
        hours += 5/60*minutes # add the angle corresponding to the minutes

        theta = cmath.pi/2 - 2*hours*cmath.pi/60
        hrs_endpoint= cmath.rect(self.hrs_radius,theta)
        polar(self.canvas,center,hrs_endpoint,3,lv_colors.RED)
    
        theta = cmath.pi/2 - 2*minutes*cmath.pi/60
        min_endpoint= cmath.rect(self.min_radius,theta)
        polar(self.canvas,center,min_endpoint,3,lv_colors.RED)
    
        # clear the old hands 
        if self.oldSec != seconds:
            theta = cmath.pi/2 - 2*self.oldSec*cmath.pi/60
            sec_endpoint= cmath.rect(self.sec_radius+2,theta)
            polar(self.canvas,center,sec_endpoint,5,lv_colors.BLACK)
        
        if self.oldMin != minutes:
            theta = cmath.pi/2 - 2*self.oldMin*cmath.pi/60
            min_endpoint= cmath.rect(self.min_radius+2,theta)
            polar(self.canvas,center,min_endpoint,7,lv_colors.BLACK)
            
            theta = cmath.pi/2 - 2*self.oldHour*cmath.pi/60
            hrs_endpoint= cmath.rect(self.hrs_radius+2,theta)
            polar(self.canvas,center,hrs_endpoint,7,lv_colors.BLACK)

        # set the new hands according to the current time
    
        theta = cmath.pi/2 - 2*hours*cmath.pi/60
        hrs_endpoint= cmath.rect(self.hrs_radius,theta)
        polar(self.canvas,center,hrs_endpoint,3,lv_colors.RED)
    
        theta = cmath.pi/2 - 2*minutes*cmath.pi/60
        min_endpoint= cmath.rect(self.min_radius,theta)
        polar(self.canvas,center,min_endpoint,3,lv_colors.RED)
    
        theta = cmath.pi/2 - 2*seconds*cmath.pi/60
        sec_endpoint= cmath.rect(self.sec_radius,theta)
        polar(self.canvas,center,sec_endpoint,1,lv_colors.WHITE)
    
        self.oldSec=seconds
        self.oldMin=minutes
        self.oldHour=hours
    
        date = [year,month,day]
        if self.oldDate != date:
            # clear old date overwriting it with a black rectangle
            rect_dsc = lv.draw_rect_dsc_t()
            rect_dsc.init()
            rect_dsc.bg_color=lv_colors.BLACK
            rect_dsc.bg_opa=lv.OPA.COVER
            self.canvas.draw_rect(0,self.CANVAS_HEIGHT-30,self.CANVAS_WIDTH,20,rect_dsc)
        
            # write new date
            dateText=dayOfWeekString(weekday) + " " + str(day) + '.' + monthString(month) + ' ' + str(year)
            label_dsc = lv.draw_label_dsc_t()
            label_dsc.init()
            label_dsc.color=lv_colors.WHITE
            self.canvas.draw_text(0,self.CANVAS_HEIGHT-30,self.CANVAS_WIDTH,
                                  label_dsc,dateText,lv.label.ALIGN.CENTER)
            self.oldDate = date
