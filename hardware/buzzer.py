# Tests the buzzer & vibration motor on the t-watch 2020
# The program is part of the course on IoT at the
# University of Cape Cape, Ghana
# copyright U. Raich 26.1.2021
# This program is released under MIT license

BUZZER_PIN = 4
import machine
import time

buzzer = machine.Pin(BUZZER_PIN, machine.Pin.OUT)
buzzer_state = False
for _ in range(10):
    if buzzer_state:
        buzzer.off()
    else:
        buzzer.on()
    time.sleep_ms(500)
    buzzer_state = not buzzer_state
