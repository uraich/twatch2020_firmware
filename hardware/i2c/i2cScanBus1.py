#!/usr/bin/env python3
# an i2c scanner
# Scans all addresses on t-watch I2C bus 1 and prints the addresses of connected
# modules
# copyright U. Raich 29.9.2020
# This program is released under MIT license

from machine import Pin,SoftI2C
import sys,time
print("Scanning the I2C bus 1 on t-watch")
print("Copyright: U.Raich")
print("Released under MIT license")

scl = Pin(32)   # bus 1 on t-watch
sda = Pin(23)   # 

i2c = SoftI2C(scl,sda)
addr = i2c.scan()

print("     0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f")

j=0
for i in range (0,16):
    print('%02x'%(16*i),end=': ')
    for j in range(0,16):
        if 16*i+j in addr:
            print('%02x'%(16*i+j),end=' ')
        else:
            print("--",end=' ')
    time.sleep(0.1)
    print()
                  

