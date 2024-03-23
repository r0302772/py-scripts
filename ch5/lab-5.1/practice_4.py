import time
import wiringpi

def blink(pin, duration):
    wiringpi.digitalWrite(pin, 1)    # Turn on LED
    time.sleep(duration)             # Adjust delay for desired speed
    wiringpi.digitalWrite(pin, 0)    # Turn off LED

# Pins for LEDs
led_pins = [5, 2, 4, 3]

# SETUP
print("Start")
wiringpi.wiringPiSetup()

# Set all LED pins to mode 1 (OUTPUT)
for pin in led_pins:
    wiringpi.pinMode(pin, 1)

# MAIN
try:
    while True:
        # From left to right
        for pin in led_pins:
            blink(pin, 0.1)  # Adjust duration for desired speed
        
        # From right to left
        for pin in reversed(led_pins):
            blink(pin, 0.1)  # Adjust duration for desired speed

except KeyboardInterrupt:
    # Clean up GPIO on exit
    for pin in led_pins:
        wiringpi.digitalWrite(pin, 0)
    print("\nDone")
