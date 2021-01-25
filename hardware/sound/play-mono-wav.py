# The MIT License (MIT)
# Copyright (c) 2020 Mike Teachman
# https://opensource.org/licenses/MIT

# Purpose:
# - read 16-bit audio samples from a mono formatted WAV file on SD card
# - write audio samples to an I2S amplifier or DAC module 
#
# Sample WAV files in wav_files folder:
#   "taunt-16k-16bits-mono.wav"
#   "taunt-16k-16bits-mono-12db.wav" (lower volume version)
#
# Hardware tested:
# - MAX98357A amplifier module (Adafruit I2S 3W Class D Amplifier Breakout)
# - PCM5102 stereo DAC module
#
# The WAV file will play continuously until a keyboard interrupt is detected or
# the ESP32 is reset
  
from machine import Pin,I2S
import ttgo
from axp_constants import AXP202_VBUS_VOL_ADC1,AXP202_VBUS_CUR_ADC1,AXP202_BATT_CUR_ADC1,AXP202_BATT_VOL_ADC1

watch = ttgo.Watch()
watch = watch
tft = watch.tft
power = watch.pmu
power.adc1Enable(AXP202_VBUS_VOL_ADC1
                      | AXP202_VBUS_CUR_ADC1 
                      | AXP202_BATT_CUR_ADC1
                      | AXP202_BATT_VOL_ADC1, True)
watch.lvgl_begin()
watch.tft.backlight_fade(100)

print("enable power")
watch.enable_audio_power()
print("done")

#======= USER CONFIGURATION =======
WAV_FILE = '/wav/taunt-16k-16bits-mono-12db.wav'
SAMPLE_RATE_IN_HZ = 16000
#======= USER CONFIGURATION =======

bck_pin = Pin(26) 
ws_pin = Pin(25)  
sdout_pin = Pin(33)

# channelformat settings:
#     mono WAV:  channelformat=I2S.ONLY_LEFT

audio_out = I2S(
    I2S.NUM0, 
    bck=bck_pin, ws=ws_pin, sdout=sdout_pin, 
    standard=I2S.PHILIPS, 
    mode=I2S.MASTER_TX,
    dataformat=I2S.B16, 
    channelformat=I2S.ONLY_LEFT,
    samplerate=SAMPLE_RATE_IN_HZ,
    dmacount=10, dmalen=512)

try:
    wav = open(WAV_FILE,'rb')
    print("/wav/taunt-16k-16bits-mono-12db.wav successfully opened")
except:
    print("Could not open /wav/taunt-16k-16bits-mono-12db.wav for reading")
    sys.exit()

# advance to first byte of Data section in WAV file
pos = wav.seek(44) 

# allocate sample arrays
#   memoryview used to reduce heap allocation in while loop
wav_samples = bytearray(1024)
wav_samples_mv = memoryview(wav_samples)

print('Starting')
# continuously read audio samples from the WAV file 
# and write them to an I2S DAC
while True:
    try:
        num_read = wav.readinto(wav_samples_mv)
        num_written = 0
        # end of WAV file?
        if num_read == 0:
            # advance to first byte of Data section
            pos = wav.seek(44) 
        else:
            # loop until all samples are written to the I2S peripheral
            while num_written < num_read:
                num_written += audio_out.write(wav_samples_mv[num_written:num_read], timeout=0)
    except (KeyboardInterrupt, Exception) as e:
        print('caught exception {} {}'.format(type(e).__name__, e))
        break
    
wav.close()
audio_out.deinit()
print('Done')
