#!/usr/bin/bash
# This shell scripts sets up the t-watch application
# python modules and images are uploaded to the t-watch
# Demo program for the course on the Internet of Things (IoT) at the
# University of Cape Coast (Ghana)
# Copyright (c) U. Raich April 2020
# This program is released under the MIT license

echo "Setting up the file system for the t-watch program"
dirs="$(ampy ls)"
echo $dirs
#
# check if /lib already exists, create it if not
#
if [[ $dirs == *"/lib"* ]]
then
    echo "/lib directory already exists"
else
    echo "Creating /lib directory"
    ampy mkdir /lib
fi

if [[ $dirs == *"/gui"* ]]
then
    echo "/gui directory already exists"
else
    echo "Creating /gui directory"
    ampy mkdir /gui
fi
echo "Uploading the constants"
ampy put src/constants.py constants.py

echo "-----------------------------"
echo "Uploading python code to /gui"
echo "-----------------------------"
echo "Uploading  src/gui/app.py"
ampy put src/gui/app.py /gui/app.py
echo "Uploading  src/gui/gui.py"
ampy put src/gui/gui.py /gui/gui.py
echo "Uploading  src/gui/splashscreen.py"
ampy put src/gui/splashscreen.py /gui/splashscreen.py
echo "Uploading  src/gui/statusbar.py"
ampy put src/gui/statusbar.py /gui/statusbar.py
echo "Uploading  src/gui/__init__.py"
ampy put src/gui/__init__.py /gui/__init__.py

if [[ $dirs == *"/app"* ]]
then
    echo "/app directory already exists"
else
    echo "Creating /app directory"
    ampy mkdir /app
fi

#
# check if the /images folder exists, create it if not
#
if [[ $dirs == *"/images"* ]]
then
    echo "/images directory already exists"
    images="$(ampy ls /images)"
    
else
    echo "Creating /images directory"
    ampy mkdir /images
    images=""
fi
#
# check it images have already been uploaded, upload them if not
#
if echo $images | grep -w "hedgehog143x81_argb565.bin" > /dev/null ; then
    echo "hedgehog143x81_argb565.bin has already been uploaded"
else
    echo "Uploading hedgehog143x81_argb565.bin"
    ampy put src/images/hedgehog143x81_argb565.bin /images/hedgehog143x81_argb565.bin
fi
#
# wallpapers
#

echo "uploading wallpapers"

if echo $images | grep -w "bg1_240px_rgb565.bin" > /dev/null ; then
    echo "bg1_240px_rgb565.bin has already been uploaded"
else
    echo "Uploading bg1_240px_rgb565.bin"
    ampy put src/images/bg1_240px_rgb565.bin /images/bg1_240px_rgb565.bin
fi
if echo $images | grep -w "bg2_240px_rgb565.bin" > /dev/null ; then
    echo "bg2_240px_rgb565.bin has already been uploaded"
else
    echo "Uploading bg2_240px_rgb565.bin"
    ampy put src/images/bg2_240px_rgb565.bin /images/bg2_240px_rgb565.bin
fi
if echo $images | grep -w "bg3_240px_rgb565.bin" > /dev/null ; then
    echo "bg3_240px_rgb565.bin has already been uploaded"
else
    echo "Uploading bg3_240px_rgb565.bin"
    ampy put src/images/bg3_240px_rgb565.bin /images/bg3_240px_rgb565.bin
fi

echo "---------------------------"
echo "uploading application icons"
echo "---------------------------"

if echo $images | grep -w "message_64px_argb565.bin" > /dev/null ; then
    echo "message_64pxargb565.bin has already been uploaded"
else
    echo "Uploading message_argb565.bin"
    ampy put src/images/message_64px_argb565.bin /images/message_64px_argb565.bin
fi

if echo $images | grep -w "weather_64px_argb565.bin" > /dev/null ; then
    echo "weather_64px_argb565.bin has already been uploaded"
else
    echo "Uploading weather_argb565.bin"
    ampy put src/images/weather_64px_argb565.bin /images/weather_64px_argb565.bin
fi

if echo $images | grep -w "mondaine_clock_64px_argb565.bin" > /dev/null ; then
    echo "mondaine_clock_64px_argb565.bin has already been uploaded"
else
    echo "Uploading mondaine_clock_64px_argb565.bin"
    ampy put src/images/mondaine_clock_64px_argb565.bin /images/mondaine_clock_64px_argb565.bin
fi

if echo $images | grep -w "stopwatch_64px_argb565.bin" > /dev/null ; then
    echo "stopwatch_64px_argb565.bin has already been uploaded"
else
    echo "Uploading stopwatch_64px_argb565.bin"
    ampy put src/images/stopwatch_64px_argb565.bin /images/stopwatch_64px_argb565.bin
fi

if echo $images | grep -w "alarm_clock_64px_argb565.bin" > /dev/null ; then
    echo "alarm_clock_64px_argb565.bin has already been uploaded"
else
    echo "Uploading alarm_clock_64px_argb565.bin"
    ampy put src/images/alarm_clock_64px_argb565.bin /images/alarm_clock_64px_argb565.bin
fi

if echo $images | grep -w "calendar_64px_argb565.bin" > /dev/null ; then
    echo "calendar_64px_argb565.bin has already been uploaded"
else
    echo "Uploading calendar_64px_argb565.bin"
    ampy put src/images/calendar_64px_argb565.bin /images/calendar_64px_argb565.bin
fi

if echo $images | grep -w "powermeter_64px_argb565.bin" > /dev/null ; then
    echo "powermeter_argb565.bin has already been uploaded"
else
    echo "Uploading powermeter_64px_argb565.bin"
    ampy put src/images/powermeter_64px_argb565.bin /images/powermeter_64px_argb565.bin
fi

if echo $images | grep -w "calculator_64px_argb565.bin" > /dev/null ; then
    echo "calculator_64px_argb565.bin has already been uploaded"
else
    echo "Uploading calculator_64px_argb565.bin"
    ampy put src/images/calculator_64px_argb565.bin /images/calculator_64px_argb565.bin
fi

if echo $images | grep -w "status_64px_argb565.bin" > /dev/null ; then
    echo "status_64px_argb565.bin has already been uploaded"
else
    echo "Uploading status_64px_argb565.bin"
    ampy put src/images/status_64px_argb565.bin /images/status_64px_argb565.bin
fi

echo "---------------------"
echo "uploading setup icons"
echo "---------------------"

if echo $images | grep -w "battery_icon_64px_argb565.bin" > /dev/null ; then
    echo "battery_icon_65px_argb565.bin has already been uploaded"
else
    echo "Uploading battery_icon_64px_argb565.bin"
    ampy put src/images/battery_icon_64px_argb565.bin /images/battery_icon_64px_argb565.bin
fi

if echo $images | grep -w "brightness_64px_argb565.bin" > /dev/null ; then
    echo "brightness_64px_argb565.bin has already been uploaded"
else
    echo "Uploading brightness_64px_argb565.bin"
    ampy put src/images/brightness_64px_argb565.bin images/brightness_64px_argb565.bin
fi

if echo $images | grep -w "move_64px_argb565.bin" > /dev/null ; then
    echo "move_64px_argb565.bin has already been uploaded"
else
    echo "Uploading move_64px_argb565.bin"
    ampy put src/images/move_64px_argb565.bin images/move_64px_argb565.bin
fi

if echo $images | grep -w "wifi_64px_argb565.bin" > /dev/null ; then
    echo "wifi_64px_argb565.bin has already been uploaded"
else
    echo "Uploading wifi_64px_argb565.bin"
    ampy put src/images/wifi_64px_argb565.bin images/wifi_64px_argb565.bin
fi

if echo $images | grep -w "bluetooth_64px_argb565.bin" > /dev/null ; then
    echo "bluetooth_64_px_argb565.bin has already been uploaded"
else
    echo "Uploading bluetooth_argb565.bin"
    ampy put src/images/bluetooth_64px_argb565.bin images/bluetooth_64px_argb565.bin
fi

if echo $images | grep -w "time_64px_argb565.bin" > /dev/null ; then
    echo "time_64px_argb565.bin has already been uploaded"
else
    echo "Uploading time_64px_argb565.bin"
    ampy put src/images/time_64px_argb565.bin images/time_64px_argb565.bin
fi

if echo $images | grep -w "update_64px_argb565.bin" > /dev/null ; then
    echo "update_64px_argb565.bin has already been uploaded"
else
    echo "Uploading update_64px_argb565.bin"
    ampy put src/images/update_64px_argb565.bin images/update_64px_argb565.bin
fi

if echo $images | grep -w "utilities_64px_argb565.bin" > /dev/null ; then
    echo "utilities_64px_argb565.bin has already been uploaded"
else
    echo "Uploading utilities_64px_argb565.bin"
    ampy put src/images/utilities_64px_argb565.bin images/utilities_64px_argb565.bin
fi
if echo $images | grep -w "sound_64px_argb565.bin" > /dev/null ; then
    echo "sound_64px_argb565.bin has already been uploaded"
else
    echo "Uploading sound_64px_argb565.bin"
    ampy put src/images/sound_64px_argb565.bin images/sound_64px_argb565.bin
fi

if echo $images | grep -w "exit_32px_argb565.bin" > /dev/null ; then
    echo "exit_32px_argb565.bin has already been uploaded"
else
    echo "Uploading exit_32px_argb565.bin"
    ampy put src/images/exit_32px_argb565.bin images/exit_32px_argb565.bin
fi

if echo $images | grep -w "setup_32px_argb565.bin" > /dev/null ; then
    echo "setup_32px_argb565.bin has already been uploaded"
else
    echo "Uploading setup_32px_argb565.bin"
    ampy put src/images/setup_32px_argb565.bin images/setup_32px_argb565.bin
fi

if echo $images | grep -w "foot_16px_argb565.bin" > /dev/null ; then
    echo "foot_16px_argb565.bin has already been uploaded"
else
    echo "Uploading foot_16px_argb565.bin"
    ampy put src/images/foot_16px_argb565.bin images/foot_16px_argb565.bin
fi

dirs="$(ampy ls /gui)"
echo "dirs in /gui:"
echo dirs

if [[ $dirs == *"/mainbar"* ]]
then
    echo "/gui/mainbar directory already exists"
else
    echo "Creating /gui/mainbar directory"
    ampy mkdir /gui/mainbar
fi
echo "--------------------------------------"
echo "uploading python code to /gui/mainbar "
echo "--------------------------------------"
echo "uploading src/gui/mainbar/mainbar.py"
ampy put src/gui/mainbar/mainbar.py  /gui/mainbar/mainbar.py
echo "uploading src/gui/mainbar/__init__.py"
ampy put src/gui/mainbar/__init__.py  /gui/mainbar/__init__

dirs="$(ampy ls /gui/mainbar)"

if [[ $dirs == *"/app_tile"* ]]
then
    echo "/gui/mainbar/app_tile directory already exists"
else
    echo "Creating /gui/mainbar/app_tile directory"
    ampy mkdir /gui/mainbar/app_tile
fi

echo "Uploading src/gui/mainbar/app_tile/app_tile.py"
ampy put src/gui/mainbar/app_tile/app_tile.py /gui/mainbar/app_tile/app_tile.py

if [[ $dirs == *"/main_tile"* ]]
then
    echo "/gui/mainbar/main_tile directory already exists"
else
    echo "Creating /gui/mainbar/main_tile directory"
    ampy mkdir /gui/mainbar/main_tile
fi
echo "Uploading src/gui/mainbar/main_tile/main_tile.py"
ampy put src/gui/mainbar/main_tile/main_tile.py /gui/mainbar/main_tile/main_tile.py

if [[ $dirs == *"/note_tile"* ]]
then
    echo "/gui/mainbar/note_tile directory already exists"
else
    echo "Creating /gui/mainbar/note_tile directory"
    ampy mkdir /gui/mainbar/note_tile
fi
echo "Uploading src/gui/mainbar/note_tile/note_tile.py"
ampy put src/gui/mainbar/note_tile/note_tile.py /gui/mainbar/note_tile/note_tile.py

if [[ $dirs == *"/setup_tile"* ]]
then
    echo "/gui/mainbar/setup_tile directory already exists"
else
    echo "Creating /gui/mainbar/setup_tile directory"
    ampy mkdir /gui/mainbar/setup_tile
fi
echo "Uploading src/gui/mainbar/setup_tile/setup_tile.py"
ampy put src/gui/mainbar/setup_tile/setup_tile.py /gui/mainbar/setup_tile/setup_tile.py

dirs="$(ampy ls /gui/mainbar/setup_tile)"
if [[ $dirs == *"/battery_settings"* ]]
then
    echo "/gui/mainbar/setup_tile/battery_settings directory already exists"
else
    echo "Creating /gui/mainbar/setup_tile/battery_settings directory"
    ampy mkdir /gui/mainbar/setup_tile/battery_settings    
fi

echo "Uploading src/gui/mainbar/setup_tile/battery_settings/battery_settings.py"
ampy put src/gui/mainbar/setup_tile/battery_settings/battery_settings.py /gui/mainbar/setup_tile/battery_settings/battery_settings.py
echo "Uploading src/gui/mainbar/setup_tile/battery_settings/battery_view.py"
ampy put src/gui/mainbar/setup_tile/battery_settings/battery_view.py /gui/mainbar/setup_tile/battery_settings/battery_view.py
