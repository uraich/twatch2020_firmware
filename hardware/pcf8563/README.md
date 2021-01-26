# Had to modify the PCF8563 driver!
The pcf8563 driver was originally written by Lewis Xhe <url>https://github.com/lewisxhe/PCF8563_PythonLibrary</url>
I had some problems with the parameter sequence of the methods datetime(), set_datetime() and write_all(), which did not reflect the sequence of 
utime.localtime() which is: (year,month,date,hours,minutes,seconds,day_of_week).
I therefore modified those methods to be conform with utime.localtime()
The modified version of Lewis' pcf8563 driver is found here. 
Living the the CET (Central European Time) zone, I wrote a simple script to convert GMT to CET. This script is also added here.
