#!/opt/bin/lv_micropython
import ujson as json
import network
import uerrno
from ntptime import settime
import utime as time

class WiFi():
  NETWORKLIST_ENTRIES = 10
  def __init__(self):
    self.network_list = []
    with open('json/wifi_config.json') as f:
      data = json.load(f)  
    # print(data)
    self.enable_on_standby = data["enable_on_standby"]
    self.ftpserver = data["ftpserver"]
    self.ftpuser = data["ftpuser"]
    self.ftppass = data["ftppass"]
    self.webserver = data["webserver"]
    self.hostname = data["hostname"]
    
    for i in range(self.NETWORKLIST_ENTRIES):
      self.network_list.append(data["network_list"][i])

  def print_config(self):
    if self.ftpserver:
      print("ftp server is enabled")
      print("ftp user: ",self.ftpuser)
      print("ftp password: ",self.ftppass)        
    else:
      print("ftp server is disabled")
    print("Host name: ",self.hostname)
      
    if self.webserver:
      print("WEB server is enabled")
    else:
      print("WEB server is disabled")

  def connect(self):
    station = network.WLAN(network.STA_IF)
    if station.isconnected() == True:
      self.ipaddr = station.ifconfig()[0]
      print("Already connected")
      return
    
    if station.active():
      print("Station is already active")
    else:
      print ("Activating station")
      if not station.active(True):
        print("Cannot activate station! giving up ...")
        raise OSError("Cannot activate WiFi station")
        return
    # get the list of access points and compare them to the configuration
    accessPoints = station.scan()
    print(len(accessPoints), "access points found")
    
    found = False
    for i in range(len(accessPoints)):
      if found:
        break
      print("access point from scan: "+str(accessPoints[i][0],'utf-8'))
      for j in range(self.NETWORKLIST_ENTRIES):
        if str(accessPoints[i][0],'utf-8') == self.network_list[j]["ssid"]:
          print("Connecting to ",self.network_list[j]["ssid"])
          station.connect(self.network_list[j]["ssid"],self.network_list[j]["psk"])
          # wait for the connection 
          while station.isconnected() == False:
            pass
          self.ipaddr = station.ifconfig()[0]
          print("IP address: ",self.ipaddr)
          found = True
          break
    if not found:
      raise OSError("No valid access point found")

  def getIPAddress(self):
      return self.ipaddr

  def getTime(self):
    for i in range(10):
      try:
        settime()
        print("Successfully retrieved the time")
        break;
      except OSError as e:
        if e.args[0] == uerrno.ETIMEDOUT:
          print("Timeout when trying to get the time from ntp, re-trying")
          time.sleep(5)

    def gmtTime(self):
      return time.localtime(time.time())

  def cetTime(self):
    # print the time and date
    now=time.time()
    
    # correct for CET time zone
    year = time.localtime()[0]       #get current year

    HHMarch   = time.mktime((year,3 ,(31-(int(5*year/4+4))%7),1,0,0,0,0,0)) #Time of March change to CEST
    HHOctober = time.mktime((year,10,(31-(int(5*year/4+1))%7),1,0,0,0,0,0)) #Time of October change to CET
    now=time.time()
    if now < HHMarch :               # we are before last sunday of march
        cet=time.localtime(now+3600) # CET:  UTC+1H
    elif now < HHOctober :           # we are before last sunday of october
        cet=time.localtime(now+7200) # CEST: UTC+2H
    else:                            # we are after last sunday of october
        cet=time.localtime(now+3600) # CET:  UTC+1H
    return cet

  def dateString(self,dateTime):
    monthTable={1: "Jan",
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
                12: "Dec"}
    dateStr = '{:02d} {:s} {:4d} {:02d}:{:02d}:{:02d}'.format(dateTime[2],monthTable[dateTime[1]],dateTime[0],
                                                          dateTime[3],dateTime[4],dateTime[5])
    return dateStr

