# pico_w_distance_alert_final.py
from machine import Pin
import time

# Setup
trig = Pin(15, Pin.OUT)
echo = Pin(14, Pin.IN)
led = Pin(13, Pin.OUT)  # Pico W built-in LED

# Settings
ALERT_DISTANCE = 30  # cm

print("PICO W Distance Alert Starting...")
print("Bring hand within 15cm of sensor")

# Test LED immediately
led.value(1)
time.sleep(0.5)
led.value(0)
time.sleep(0.5)

# Main loop
while True:
    # Send pulse
    trig.value(0)
    time.sleep_us(2)
    trig.value(1)
    time.sleep_us(10)
    trig.value(0)
    
    # Wait for echo
    timeout = time.ticks_us() + 30000
    while echo.value() == 0:
        if time.ticks_us() > timeout:
            break
    
    start = time.ticks_us()
    
    timeout = start + 30000
    while echo.value() == 1:
        if time.ticks_us() > timeout:
            break
    
    end = time.ticks_us()
    
    # Calculate
    duration = end - start
    distance = (duration * 0.0343) / 2
    
    # Check distance
    if 2 < distance < 500:
        if distance < ALERT_DISTANCE:
            print(f"⚠️  {distance:.1f}cm - TOO CLOSE!")
            # Blink LED
            led.value(1)
            time.sleep(0.1)
            led.value(0)
            time.sleep(0.1)
        else:
            print(f"✅ {distance:.1f}cm - Safe")
            led.value(0)
            time.sleep(0.5)
    else:
        print("No valid reading")
        time.sleep(0.5)
