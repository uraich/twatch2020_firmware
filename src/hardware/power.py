#!/opt/bin/lv_micropython -i
import lvgl as lv
import display_driver
import os
from hardware.powermgr import PowerManager
import ulogging as logging
log = logging.getLogger("power")
log.setLevel(logging.DEBUG)            
#
# get access to the pmu
#
powermgr = PowerManager()
#
# enable coulomb conter and ser target voltage for charging
#


# create labels showing battery status
if powermgr.EnableCoulombcounter()

battery_style = lv.style_t()
battery_style.set_border_width(lv.obj.PART.MAIN, 0)
#
# design capacity
#
battery_design_cont = lv.obj(lv.scr_act(), None)
battery_design_cont.set_size(lv.scr_act().get_disp().driver.hor_res,25)
battery_design_cont.add_style(lv.obj.PART.MAIN,battery_style)

battery_design_cap_label = lv.label(battery_design_cont,None)
battery_design_cap_label.add_style(lv.obj.PART.MAIN,battery_style)
battery_design_cap_label.set_text("designed capacity")
battery_design_cap_label.align(battery_design_cont,lv.ALIGN.IN_LEFT_MID, 5, 0)

battery_view_design_cap = lv.label(battery_design_cont, None)
battery_view_design_cap.add_style(lv.obj.PART.MAIN,battery_style)
battery_view_design_cap.set_text("300mAh")
battery_view_design_cap.align(battery_design_cont,lv.ALIGN.IN_RIGHT_MID, -5, 0)
#
# battery current
#
battery_current_cont = lv.obj(lv.scr_act(), None)
battery_current_cont.set_size(lv.scr_act().get_disp().driver.hor_res,22)
battery_current_cont.add_style(lv.obj.PART.MAIN,battery_style)
battery_current_cont.align(battery_design_cont, lv.ALIGN.OUT_BOTTOM_MID, 0, 0 )

battery_current_cap_label = lv.label(battery_current_cont,None)
battery_current_cap_label.add_style(lv.obj.PART.MAIN,battery_style)
battery_current_cap_label.set_text("charged capacity")
battery_current_cap_label.align(battery_current_cont,lv.ALIGN.IN_LEFT_MID, 5, 0)

battery_view_current_cap = lv.label(battery_current_cont, None)
battery_view_current_cap.add_style(lv.obj.PART.MAIN,battery_style)
battery_view_current_cap.set_text("300mAh")
battery_view_current_cap.align(battery_current_cont,lv.ALIGN.IN_RIGHT_MID, -5, 0)
#
# battery voltage
#
battery_voltage_cont = lv.obj(lv.scr_act(), None)
battery_voltage_cont.set_size(lv.scr_act().get_disp().driver.hor_res,22)
battery_voltage_cont.add_style(lv.obj.PART.MAIN,battery_style)
battery_voltage_cont.align(battery_current_cont, lv.ALIGN.OUT_BOTTOM_MID, 0, 0 )

battery_voltage_cap_label = lv.label(battery_voltage_cont,None)
battery_voltage_cap_label.add_style(lv.obj.PART.MAIN,battery_style)
battery_voltage_cap_label.set_text("battery voltage")
battery_voltage_cap_label.align(battery_voltage_cont,lv.ALIGN.IN_LEFT_MID, 5, 0)

battery_view_voltage_cap = lv.label(battery_voltage_cont, None)
battery_view_voltage_cap.add_style(lv.obj.PART.MAIN,battery_style)
battery_view_voltage_cap.set_text("2.4 mV")
battery_view_voltage_cap.align(battery_voltage_cont,lv.ALIGN.IN_RIGHT_MID, -5, 0)
#
# battery charge
#
battery_charge_cont = lv.obj(lv.scr_act(), None)
battery_charge_cont.set_size(lv.scr_act().get_disp().driver.hor_res,22)
battery_charge_cont.add_style(lv.obj.PART.MAIN,battery_style)
battery_charge_cont.align(battery_voltage_cont, lv.ALIGN.OUT_BOTTOM_MID, 0, 0 )

battery_charge_cap_label = lv.label(battery_charge_cont,None)
battery_charge_cap_label.add_style(lv.obj.PART.MAIN,battery_style)
battery_charge_cap_label.set_text("charge current")
battery_charge_cap_label.align(battery_charge_cont,lv.ALIGN.IN_LEFT_MID, 5, 0)

battery_view_charge_cap = lv.label(battery_charge_cont, None)
battery_view_charge_cap.add_style(lv.obj.PART.MAIN,battery_style)
battery_view_charge_cap.set_text("100 mA")
battery_view_charge_cap.align(battery_charge_cont,lv.ALIGN.IN_RIGHT_MID, -5, 0)
#
# battery discharge
#
battery_discharge_cont = lv.obj(lv.scr_act(), None)
battery_discharge_cont.set_size(lv.scr_act().get_disp().driver.hor_res,22)
battery_discharge_cont.add_style(lv.obj.PART.MAIN,battery_style)
battery_discharge_cont.align(battery_charge_cont, lv.ALIGN.OUT_BOTTOM_MID, 0, 0 )

battery_discharge_cap_label = lv.label(battery_discharge_cont,None)
battery_discharge_cap_label.add_style(lv.obj.PART.MAIN,battery_style)
battery_discharge_cap_label.set_text("discharge current")
battery_discharge_cap_label.align(battery_discharge_cont,lv.ALIGN.IN_LEFT_MID, 5, 0)

battery_view_discharge_cap = lv.label(battery_discharge_cont, None)
battery_view_discharge_cap.add_style(lv.obj.PART.MAIN,battery_style)
battery_view_discharge_cap.set_text("100 mA")
battery_view_discharge_cap.align(battery_discharge_cont,lv.ALIGN.IN_RIGHT_MID, -5, 0)

#
# vbus voltage
#
vbus_voltage_cont = lv.obj(lv.scr_act(), None)
vbus_voltage_cont.set_size(lv.scr_act().get_disp().driver.hor_res,22)
vbus_voltage_cont.add_style(lv.obj.PART.MAIN,battery_style)
vbus_voltage_cont.align(battery_discharge_cont, lv.ALIGN.OUT_BOTTOM_MID, 0, 0 )

vbus_voltage_cap_label = lv.label(vbus_voltage_cont,None)
vbus_voltage_cap_label.add_style(lv.obj.PART.MAIN,battery_style)
vbus_voltage_cap_label.set_text("VBUS voltage")
vbus_voltage_cap_label.align(vbus_voltage_cont,lv.ALIGN.IN_LEFT_MID, 5, 0)

battery_view_discharge_cap = lv.label(vbus_voltage_cont, None)
battery_view_discharge_cap.add_style(lv.obj.PART.MAIN,battery_style)
battery_view_discharge_cap.set_text("2.4 mV")
battery_view_discharge_cap.align(vbus_voltage_cont,lv.ALIGN.IN_RIGHT_MID, -5, 0)

def battery_view_update_task():
    pass
