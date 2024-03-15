import time
import wiringpi

def blink(pins, duration):
    for pin in pins:
        wiringpi.digitalWrite(pin, 1)    # Turn on LED
    time.sleep(duration)                 # Wait for the specified duration
    for pin in pins:
        wiringpi.digitalWrite(pin, 0)    # Turn off LED

# Pins for LEDs
led_pins = [[5, 4], [2, 3]]

# SETUP
print("Start")
wiringpi.wiringPiSetup()

# Set all LED pins to mode 1 (OUTPUT)
for pins in led_pins:
    for pin in pins:
        wiringpi.pinMode(pin, 1)

# MAIN
try:
    while True:
        # First sequence: LED1 and LED3
        time.sleep(1)
        blink(led_pins[0], 0.5)  # Adjust duration for desired speed
        
        # Second sequence: LED2 and LED4 with an interval of 1 second
        time.sleep(1)
        blink(led_pins[1], 0.5)  # Adjust duration for desired speed

except KeyboardInterrupt:
    # Clean up GPIO on exit
    for pins in led_pins:
        for pin in pins:
            wiringpi.digitalWrite(pin, 0)
    print("\nDone")
