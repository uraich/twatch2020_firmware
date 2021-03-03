#!/opt/bin/lv_micropython
# create the pmu config json file

SILENCEWAKEINTERVAL = 45      # silence wakeup interval in minutes
SILENCEWAKEINTERVAL_PLUG = 3  # silence wakeup interval in minutes when plugged
NORMALVOLTAGE = 3300 
EXPERIMENTALNORMALVOLTAGE = 3000
NORMALPOWERSAVEVOLTAGE    = 3000
EXPERIMENTALPOWERSAVEVOLTAGE = 2800
import ujson as json

config = {'silence_wakeup': False,
          'silence_wakeup_interval': SILENCEWAKEINTERVAL,
          'silence_wakeup_interval_vbplug': SILENCEWAKEINTERVAL_PLUG,
          'experimental_power_save': False,
          'compute_percent': False,
          'high_charging_target_voltage': False,
          'designed_battery_cap': 300,
          'normal_voltage': NORMALVOLTAGE,
          'normal_powersave_voltage': NORMALPOWERSAVEVOLTAGE,
          'experimental_powersave_voltage': EXPERIMENTALPOWERSAVEVOLTAGE,
          'pmu_logging': False
}

print(config)
with open('pmu_config.json','w') as json_file:
    json.dump(config,json_file)

#print(config_json)
