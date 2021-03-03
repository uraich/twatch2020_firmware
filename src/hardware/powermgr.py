import lvgl as lv
try:
    from lv_colors import lv_colors
    from axp_constants import AXP202_ON, AXP202_OFF
    from axp_constants import AXP202_BATT_VOL_ADC1,AXP202_BATT_CUR_ADC1,AXP202_VBUS_VOL_ADC1,AXP202_VBUS_CUR_ADC1
    from axp_constants import AXP202_VBUS_REMOVED_IRQ,AXP202_VBUS_CONNECT_IRQ,AXP202_CHARGING_FINISHED_IRQ,\
        AXP202_CHARGING_IRQ,AXP202_TIMER_TIMEOUT_IRQ
    from axp_constants import AXP202_TARGET_VOL_4_36V,AXP202_TARGET_VOL_4_2V,AXP_ADC_SAMPLING_RATE_200HZ
    from axp_constants import AXP202_EXTEN,AXP202_DCDC2,AXP202_LDO4,AXP202_LDO3_MODE_DCIN,AXP202_LDO3
    from machine import Pin
except:
    pass

import ulogging as logging
import ujson as json

import sys
class PowerManager():
    AXP202_INT = 35
    def __init__(self,drv):
        # create a logger
        self.log = logging.getLogger("PowerManager")
        self.log.setLevel(logging.DEBUG)
        self.read_config()
        self.print_config()
        
        self.power = drv.watch.pmu
        self.power.adc1Enable( AXP202_BATT_VOL_ADC1 | AXP202_BATT_CUR_ADC1 | AXP202_VBUS_VOL_ADC1 | AXP202_VBUS_CUR_ADC1,True)
        self.power.enableIRQ(AXP202_VBUS_REMOVED_IRQ | AXP202_VBUS_CONNECT_IRQ | AXP202_CHARGING_FINISHED_IRQ | AXP202_CHARGING_IRQ | AXP202_TIMER_TIMEOUT_IRQ, AXP202_ON)
        self.power.clearIRQ()
        #
        # enable Coulomb counter and set target voltage for charging
        #
        if self.power.EnableCoulombcounter():
            self.log.error("enabling the Coulomb counter failed!")
        if self.config['high_charging_target_voltage']:
            self.log_info('set target voltage to 4.36V')
            if self.power.setChargingTargetVoltage(AXP202_TARGET_VOL_4_36V):
                self.log.error("target voltage 4.36V set failed!")
        else:
            self.log.info('set target voltage to 4.2V')
            if self.power.setChargingTargetVoltage(AXP202_TARGET_VOL_4_2V):
                self.log.error("target voltage 4.2V set failed!")
        if self.power.setChargeControlCur(300):
            self.log.error("charge current set failed!")
        if self.power.setAdcSamplingRate(AXP_ADC_SAMPLING_RATE_200HZ):
            self.log.error("adc sample set failed!")
        #
        # switch off unused power
        #
        self.log.debug("Switch off unused power")
        self.power.setPowerOutPut(AXP202_EXTEN, AXP202_OFF)
        self.power.setPowerOutPut(AXP202_DCDC2, AXP202_OFF)
        self.power.setPowerOutPut(AXP202_LDO4, AXP202_OFF)
        #
        # turn i2s DAC on
        #
        self.log.debug("Switch i2s DAC on")
        self.power.setLDO3Mode(AXP202_LDO3_MODE_DCIN)
        self.power.setPowerOutPut(AXP202_LDO3, AXP202_ON)
        #
        # register IRQ function and GPIO pin
        #
        self.pmu_int = Pin(self.AXP202_INT,Pin.IN,Pin.PULL_UP)
        self.pmu_int.irq(trigger=Pin.IRQ_FALLING, handler=self.pmu_irq_cb)

    def pmu_irq_cb(self):
        print("pmu_irq")
        
    def read_config(self):
        with open('json/pmu_config.json') as f:
            self.config = json.load(f)

    def print_config(self):
        print("-------------------")
        print("power configuration")
        print("-------------------")
        if self.config['silence_wakeup']:
            print("Silence wakeup is switched on")
        else:
            print("Silence wakeup is switched off")
        print("Silence wakeup interval: %d mins"%self.config['silence_wakeup_interval'])
        print("Silence wakeup interval when plugged into VBus: %d mins"%self.config['silence_wakeup_interval_vbplug'])
        if self.config['experimental_power_save']:
            print("Experimental power save mode is switched on")
        else:
            print("Experimental power save mode is switched off")
        
        if self.config['compute_percent']:
             print("Compute percent is switched on")
        else:
            print("Compute percent is switched off")
        
        if self.config['high_charging_target_voltage']:
             print("High charging target voltage is enabled")
        else:
            print("Normal charging voltage")       

        print("Design battery capacity: %d mAh"%self.config['designed_battery_cap'])
        print("Normal voltage: %d mV"%self.config['normal_voltage'])
        print("Normal power save voltage: %d mV"%self.config['normal_powersave_voltage'])
        print("Experimental power save voltage: %d mV"%self.config['experimental_powersave_voltage'])
        if self.config['pmu_logging']:
            print("PMU logging is on")
        else:
            print("PMU logging is off")
        
        
    def write_config(self):
        with open('json/pmu_config.json') as f:
            json.dump(self.config,f)

        
