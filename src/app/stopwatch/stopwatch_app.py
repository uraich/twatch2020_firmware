#!/opt/bin/lv_micropython -i
import lvgl as lv
from lv_colors import lv_colors
from gui.icon import Icon
import utime as time

class Stopwatch():
    def __init__(self,mainbar):
        try:
            import ulogging as logging
        except:
            import logging
             
        self.log = logging.getLogger("Stopwatch")
        self.log.setLevel(logging.DEBUG)
        
        self.mainbar=mainbar
        self.statusbar=mainbar.gui.statusbar
        self.app = mainbar.app
        
        self.tile_num = mainbar.add_app_tile( 1, 1, "Stopwatch App" )
        self.log.debug("tile number for main tile: %d",self.tile_num)
        self.stopwatch_tile = mainbar.get_tile_obj(self.tile_num)

        self.stopwatch_style = lv.style_t()
        self.stopwatch_style.copy(self.mainbar.get_style())
        self.stopwatch_style.set_text_font(lv.STATE.DEFAULT,lv.font_montserrat_48)
        
        # create the container
        self.stopwatch_cont = lv.obj(self.stopwatch_tile,None)
        self.stopwatch_cont.set_size(lv.scr_act().get_disp().driver.hor_res,
                                lv.scr_act().get_disp().driver.ver_res//2)
        
        self.stopwatch_cont.add_style(lv.obj.PART.MAIN,self.stopwatch_style)
        self.stopwatch_cont.align(self.stopwatch_tile,lv.ALIGN.CENTER, 0, 0)
        
        self.label = lv.label(self.stopwatch_cont,None)
        self.label.set_text("00:00.0")
        self.label.align(self.stopwatch_cont,lv.ALIGN.CENTER, 0, 0)
        self.label.add_style(lv.obj.PART.MAIN,self.stopwatch_style)
        # create exit button
        self.exit_btn = lv.imgbtn(self.stopwatch_tile,None)        
        self.exit_btn.set_src(lv.btn.STATE.RELEASED,self.mainbar.get_exit_btn_dsc())
        self.exit_btn.add_style(lv.imgbtn.PART.MAIN,self.stopwatch_style)
        self.exit_btn.align(self.stopwatch_tile,lv.ALIGN.IN_BOTTOM_LEFT, 10, -10 )
        self.log.debug("setting up exit callback")
        self.exit_btn.set_event_cb(self.exit_stopwatch_app_event_cb)
        # create start button
        self.start_button = lv.btn(self.stopwatch_tile,None)
        self.start_button.set_size(50, 50)
        self.symbol_style = lv.style_t()
        self.symbol_style.copy(self.stopwatch_style)
        self.symbol_style.set_text_font(lv.STATE.DEFAULT,lv.font_montserrat_32)
        self.start_button.add_style(lv.imgbtn.PART.MAIN, self.symbol_style )
        self.start_button.align(self.stopwatch_tile, lv.ALIGN.IN_BOTTOM_MID, 0, 0 )
        self.start_button.set_event_cb(self.start_stopwatch_event_cb)
        self.start_button_label = lv.label(self.start_button,None)
        self.start_button_label.set_text(lv.SYMBOL.PLAY)

        # create stop button
        self.stop_button = lv.btn(self.stopwatch_tile,None)
        self.stop_button.set_size(50, 50)
        self.stop_button.add_style(lv.imgbtn.PART.MAIN, self.symbol_style )
        self.stop_button.align(self.stopwatch_tile, lv.ALIGN.IN_BOTTOM_MID, 0, 0 )
        self.stop_button.set_event_cb(self.stop_stopwatch_event_cb)
        self.stop_button_label = lv.label(self.stop_button,None)
        self.stop_button_label.set_text(lv.SYMBOL.STOP)
        self.stop_button.set_hidden(True)
        
        # create reset button
        self.reset_button = lv.btn(self.stopwatch_tile,None)
        self.reset_button.set_size(50, 50)
        self.reset_button.add_style(lv.imgbtn.PART.MAIN, self.symbol_style )
        self.reset_button.align(self.stopwatch_tile, lv.ALIGN.IN_BOTTOM_RIGHT, -20, 0 )
        self.reset_button.set_event_cb(self.reset_stopwatch_event_cb)
        self.reset_button_label = lv.label(self.reset_button,None)
        self.reset_button_label.set_text(lv.SYMBOL.EJECT)
        self.is_running=False
        self.log.debug("registering stopwatch app")
        app=self.app.register("stop\nwatch","stopwatch_64px",self.enter_stopwatch_app_event_cb)

    def enter_stopwatch_app_event_cb(self,obj,evt):
        if evt == lv.EVENT.CLICKED:
            self.log.debug("enter_stopwatch_app_event_cb called")
            self.statusbar.hide(True)
            # self.app.hide_indicator( example_app )
            self.mainbar.jump_to_tilenumber(self.tile_num, lv.ANIM.OFF )
            
    def exit_stopwatch_app_event_cb(self,obj,evt):
        if evt == lv.EVENT.CLICKED:
            self.log.debug("exit_stopwatch_app_event_cb called")
            self.statusbar.hide(False)
            if self.is_running:
                self.stopwatch_app_task._del()
                self.start_button.set_hidden(False)
                self.stop_button.set_hidden(True)
                self.is_running = False
            # reset the stop watch
            self.label.set_text("00:00.0")
            self.mainbar.jump_to_maintile(lv.ANIM.OFF)

    def start_stopwatch_event_cb(self,obj,evt):
        if evt == lv.EVENT.CLICKED:
            self.log.debug("start_stopwatch_event_cb called")
            self.start_button.set_hidden(True)
            self.stop_button.set_hidden(False)
            # create a task that runs every second
            self.is_running=True
            self.start_time = time.time()
            self.secs = self.start_time
            self.hundred_ms = 0
            self.stopwatch_app_task = lv.task_create_basic()
            self.stopwatch_app_task.set_cb(lambda task: self.update(self.stopwatch_app_task))
            self.stopwatch_app_task.set_period(100)
            self.stopwatch_app_task.set_prio(lv.TASK_PRIO.LOWEST)

    def stop_stopwatch_event_cb(self,obj,evt):
        if evt == lv.EVENT.CLICKED:
            self.stopwatch_app_task._del()
            self.start_button.set_hidden(False)
            self.stop_button.set_hidden(True)
            self.is_running = False
        
    def reset_stopwatch_event_cb(self,obj,evt):
        if evt == lv.EVENT.CLICKED:                
            self.log.debug("reset clicked")
            # stop the stopwatch, just in case it is running
            self.label.set_text("00:00.0")           
            self.start_time = time.time()
                       
    # update the stopwatch display
    def update(self,task):
        current_time = time.time()
        elapsed_time = current_time-self.start_time
        secs = int(elapsed_time)
        hundred_ms = int(elapsed_time*10) - secs*10
        if secs >= 3600:
            # overflow, stop the stopwatch            
            self.stopwatch_app_task._del()
            self.start_button.set_hidden(False)
            self.stop_button.set_hidden(True)
            return
        minutes = secs//60
        seconds = secs % 60
        time_string = "%02d:%02d.%d"%(minutes,seconds,hundred_ms)
        self.label.set_text(time_string)

  
        
