import time
import wiringpi

# Pins for LEDs and switch
led_pins = [2, 8, 7, 5]
pin_switch = 1

# SETUP
print("Start")
wiringpi.wiringPiSetup()

# Set all LED pins to mode 1 (OUTPUT) and switch pin to mode 0 (INPUT)
for pin in led_pins:
    wiringpi.pinMode(pin, 1)
wiringpi.pinMode(pin_switch, 0)

def blink(pin, duration):
    wiringpi.digitalWrite(pin, 1)    # Turn on LED
    time.sleep(duration)             # Adjust delay for desired speed
    wiringpi.digitalWrite(pin, 0)    # Turn off LED

# MAIN
try:
    while True:
        if wiringpi.digitalRead(pin_switch) == 1:  # If GPIO2 is activated
            # From left to right
            for pin in led_pins:
                blink(pin, 0.1)  # Adjust duration for desired speed
        else:  # If GPIO2 is deactivated
            # From right to left
            for pin in reversed(led_pins):
                blink(pin, 0.1)  # Adjust duration for desired speed

except KeyboardInterrupt:
    # Clean up GPIO on exit
    for pin in led_pins:
        wiringpi.digitalWrite(pin, 0)
    print("\nDone")
