#!/opt/bin/lv_micropython
# create the wificonfig json file

import ujson as json
NETWORKLIST_ENTRIES = 10
networklist_entry = []

networklist = []*NETWORKLIST_ENTRIES
#networklist.append({'ssid':'WLAN18074253','psk':'Q4k6V35sFauw'})
#networklist.append({'ssid':'SFR_A0F0_EXT','psk':'osto7rawayristaxtris'})
for i in range(NETWORKLIST_ENTRIES):
    networklist.append({'ssid':None,'psk':None})
networklist[0]={'ssid':'WLAN18074253','psk':'Q4k6V35sFauw'}
networklist[1]={'ssid':'SFR_A0F0_EXT','psk':'osto7rawayristaxtris'}

print(networklist)
config = {'webserver': False,
          'ftpserver': False,
          'ftpuser': None,
          'ftppass': None,
          'enable_on_standby': False,
          'hostname':'t-watch_Uli',
          'network_list':networklist
          }

print(config)
with open('wifi_config.json','w') as json_file:
    json.dump(config,json_file)

#print(config_json)
