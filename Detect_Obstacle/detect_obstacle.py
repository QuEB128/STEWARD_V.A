from machine import Pin, time_pulse_us
import time

# Pins
TRIG = Pin(3, Pin.OUT)   # TRIG on GP3
ECHO = Pin(2, Pin.IN)    # ECHO on GP2
led = Pin(1, Pin.OUT)   # Onboard LED

# Function to measure distance in cm
def get_distance():
    TRIG.low()
    time.sleep_us(2)
    TRIG.high()
    time.sleep_us(10)
    TRIG.low()

    # Measure echo pulse duration
    duration = time_pulse_us(ECHO, 1, 30000)  # timeout 30ms

    # Convert to distance (cm)
    distance = (duration * 0.0343) / 2
    return distance

while True:
    dist = get_distance()
    print("Distance:", dist, "cm")  # <-- Serial monitor output

    if dist < 200:  
        led.value(1)
        time.sleep(0.1)
        led.value(0)
        led.value(1)
        time.sleep(0.1)
        led.value(0)
        time.sleep(0.2)
    else:
        led.value(0)  # LED off
        time.sleep(0.1)
