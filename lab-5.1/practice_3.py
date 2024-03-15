import time
import wiringpi

def blink(pin):
    wiringpi.digitalWrite(pin, 1)    # Turn on LED
    time.sleep(0.1)                  # Adjust delay for desired speed
    wiringpi.digitalWrite(pin, 0)    # Turn off LED
    time.sleep(0.1)                  # Adjust delay for desired speed

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
        for pin in led_pins:
            blink(pin)
except KeyboardInterrupt:
    # Clean up GPIO on exit
    for pin in led_pins:
        wiringpi.digitalWrite(pin, 0)
    print("\nDone")
