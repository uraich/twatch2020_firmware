# Sets the realtime clock PCF8563 on the t-watch 2020 to the current time
# The program is part of the course on IoT at the
# University of Cape Cape, Ghana
# copyright U. Raich 26.1.2021
# This program is released under MIT license

import utime as time
from machine import SoftI2C,Pin
from pcf8563 import PCF8563
T_WATCH_I2C0_SCL = 22
T_WATCH_I2C0_SDA = 21

month_str=["January","February","March","April","May","June","July",
           "August","September","October","November","December"]
month_short = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
day_of_week_str = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
day_of_week_short = ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"]
#
# initialize I2C bus 0 on the t-watch
#
t_watch_i2c0 = SoftI2C(scl=Pin(T_WATCH_I2C0_SCL),sda=Pin(T_WATCH_I2C0_SDA))
#
# create a pcf8563 object on the I2C0 bus
#
pcf8563 = PCF8563(t_watch_i2c0)
currentTime = pcf8563.datetime()

year = currentTime[0]
month = currentTime[1]
date = currentTime[2]
hour = currentTime[3]
minute = currentTime[4]
second = currentTime[5]
day = currentTime[6]
print("Time read from PCF8563: %s %d. %s %02d %02d:%02d:%02d"%(day_of_week_short[day],
                                 date,month_short[month],year,
                                 hour,minute,second))
print("done")
