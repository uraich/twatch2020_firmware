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
    echo "The following modules have been uploaded to /lib:"
    modules="$(ampy ls /lib)"
    for i in $modules ; do
	echo ${i#"/lib/"}
	done    
else
    echo "Creating /lib directory"
    ampy mkdir /lib
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
if echo $images | grep -w "hedgehog143x81_rgb565.bin" > /dev/null ; then
    echo "hedgehog143x81_rgb565.bin has already been uploaded"
else
    echo "Uploading hedgehog143x81_rgb565.bin"
    ampy put src/gui/images/hedgehog143x81_rgb565.bin /images/hedgehog143x81_rgb565.bin
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
