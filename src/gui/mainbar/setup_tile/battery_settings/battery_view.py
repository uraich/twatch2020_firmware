#!/opt/bin/lv_micropython -i
import lvgl as lv
from lv_colors import lv_colors
from micropython import const
from constants import Constants
try:
    import ulogging as logging
except:
    import logging

class BatteryViewTile():
    def __init__(self,parent,tile_num):
        
        self.log = logging.getLogger("BatteryViewTile")
        self.log.setLevel(logging.DEBUG)
        
        self.tile_num = tile_num;
        self.tile = parent.get_tile_obj(tile_num)

        self.style = lv.style_t()
        self.style.copy(parent.mainbar_style)
        self.style.set_bg_color(lv.obj.PART.MAIN,lv_colors.GRAY)
        self.style.set_bg_opa(lv.obj.PART.MAIN,lv.OPA.COVER)
        self.style.border_width(lv.obj.PART.MAIN,0)
        self.tile.add_style(lv.obj.PART.MAIN,self.style)
        
        # create exit button
        
        self.exit_icon = parent.get_exit_btn_dsc()
        self.exit_btn = lv.imgbtn(self.tile,None)
        self.exit_btn.set_src(lv.btn.STATE.RELEASED, self.exit_icon)
        self.exit_btn.add_style(lv.imgbtn.PART.MAIN,self.style)
        self.exit_btn.align(self.tile,lv.ALIGN.IN_TOP_LEFT, 10, Constants.STATUSBAR_HEIGHT + 10)
        
        # create settings button
        
        self.settings_icon = parent.get_setup_btn_dsc()
        self.settings_btn = lv.imgbtn(self.tile,None)
        self.settings_btn.set_src(lv.btn.STATE.RELEASED, self.exit_icon)
        self.settings_btn.add_style(lv.imgbtn.PART.MAIN,self.style)
        self.settings_btn.align(self.tile,lv.ALIGN.IN_TOP_RIGHT, -10, Constants.STATUSBAR_HEIGHT + 10)

        self.exit_label = lv.label(self.tile,None)
        self.exit_label.set_text("battery / energy")
        self.exit_label.align(self.exit_btn.lv.ALIGN.OUT_RIGHT_MID, 5, 0)
        
        self.design_cont = lv.obj(self.tile,None)
        self.design_cont.set_size(lv.scr_act().get_disp().driver.hor_res,25)
        self.design_cont.add_style(lv.obj.PART.MAIN, self.style)
        self.design_cont.align( self.tile, lv.ALIGN.IN_TOP_RIGHT, 0, 75 )
        self.design_cap_label = lv.label( self.design_cont, None)
        self.design_cap_label.add_style( lv.obj.PART.MAIN, self.style)
        self.design_cap_label.set_text( "designed cap");
        self.design_cap_label.align( self.design_cont, lv.ALIGN.IN_LEFT_MID, 5, 0)

        self.design_cap = lv.label( self.design_cont, None)
        self.design_cap.add_style( lv.obj.PART.MAIN, self.style)
        self.design_cap.set_text("300mAh");
        self.design_cap.align( self.design_cont, lv.ALIGN_IN.RIGHT_MID, -5, 0)
        
        self.current_cont = lv.obj(self.tile,None)
        self.current_cont.set_size(lv.scr_act().get_disp().driver.hor_res,22)
        self.current_cont.add_style(lv.obj.PART.MAIN, self.style)
        self.current_cont.align( self.design_cont, lv.ALIGN.OUT_BOTTOM_MID, 0, 0 )
        self.current_cap_label = lv.label( self.current_cont, None)
        self.current_cap_label.add_style( lv.obj.PART.MAIN, self.style)
        self.current_cap_label.set_text( "charged capacity");
        self.current_cap_label.align( self.current_cont, lv.ALIGN.IN_LEFT_MID, 5, 0)

        self.current_cap = lv.label( self.current_cont, None)
        self.current_cap.add_style( lv.obj.PART.MAIN, self.style)
        self.current_cap.set_text("300mAh");
        self.current_cap.align( self.current_cont, lv.ALIGN_IN.RIGHT_MID, -5, 0)

        self.voltage_cont = lv.obj(self.tile,None)
        self.voltage_cont.set_size(lv.scr_act().get_disp().driver.hor_res,22)
        self.voltage_cont.add_style(lv.obj.PART.MAIN, self.style)
        self.voltage_cont.align( self.current_cont, lv.ALIGN.OUT_BOTTOM_MID, 0, 0 )
        self.voltage_label = lv.label( self.voltage_cont, None)
        self.voltage_label.add_style( lv.obj.PART.MAIN, self.style)
        self.voltage_label.set_text( "battery voltage");
        self.voltage_label.align( self.current_cont, lv.ALIGN.IN_LEFT_MID, 5, 0)

        self.voltage = lv.label( self.current_cont, None)
        self.voltage.add_style( lv.obj.PART.MAIN, self.style)
        self.voltage.set_text("2.4mV");
        self.voltage.align( self.current_cont, lv.ALIGN_IN.RIGHT_MID, -5, 0)

        self.charge_cont = lv.obj(self.tile,None)
        self.charge_cont.set_size(lv.scr_act().get_disp().driver.hor_res,22)
        self.charge_cont.add_style(lv.obj.PART.MAIN, self.style)
        self.charge_cont.align( self.voltage_cont, lv.ALIGN.OUT_BOTTOM_MID, 0, 0 )
        self.charge_label = lv.label( self.charge_cont, None)
        self.charge_label.add_style( lv.obj.PART.MAIN, self.style)
        self.charge_label.set_text( "charge current");
        self.charge_label.align( self.current_cont, lv.ALIGN.IN_LEFT_MID, 5, 0)

        self.charge = lv.label( self.current_cont, None)
        self.charge.add_style( lv.obj.PART.MAIN, self.style)
        self.charge.set_text("100mAh");
        self.charge.align( self.current_cont, lv.ALIGN_IN.RIGHT_MID, -5, 0)

        self.discharge_cont = lv.obj(self.tile,None)
        self.discharge_cont.set_size(lv.scr_act().get_disp().driver.hor_res,22)
        self.discharge_cont.add_style(lv.obj.PART.MAIN, self.style)
        self.discharge_cont.align( self.charge_cont, lv.ALIGN.OUT_BOTTOM_MID, 0, 0 )
        self.discharge_label = lv.label( self.discharge_cont, None)
        self.discharge_label.add_style( lv.obj.PART.MAIN, self.style)
        self.discharge_label.set_text( "discharge current");
        self.discharge_label.align( self.current_cont, lv.ALIGN.IN_LEFT_MID, 5, 0)

        self.discharge = lv.label( self.current_cont, None)
        self.discharge.add_style( lv.obj.PART.MAIN, self.style)
        self.discharge.set_text("100mAh");
        self.discharge.align( self.current_cont, lv.ALIGN_IN.RIGHT_MID, -5, 0)        
        
        self.vbus_voltage_cont = lv.obj(self.tile,None)
        self.vbus_voltage_cont.set_size(lv.scr_act().get_disp().driver.hor_res,22)
        self.vbus_voltage_cont.add_style(lv.obj.PART.MAIN, self.style)
        self.vbus_voltage_cont.align( self.discharge_cont, lv.ALIGN.OUT_BOTTOM_MID, 0, 0 )
        self.vbus_voltage_label = lv.label( self.vbus_voltage_cont, None)
        self.vbus_voltage_label.add_style( lv.obj.PART.MAIN, self.style)
        self.vbus_voltage_label.set_text( "vbus_voltage current");
        self.vbus_voltage_label.align( self.current_cont, lv.ALIGN.IN_LEFT_MID, 5, 0)

        self.vbus_voltage = lv.label( self.current_cont, None)
        self.vbus_voltage.add_style( lv.obj.PART.MAIN, self.style)
        self.vbus_voltage.set_text("100mAh");
        self.vbus_voltage.align( self.current_cont, lv.ALIGN_IN.RIGHT_MID, -5, 0)        
               
