import wiringpi as wp
import time

# Set pin numbers for LEDs
led_pins = [5, 2, 4, 3]

# Initialize WiringPi
wp.wiringPiSetup()

# Set up LED pins as PWM output
for pin in led_pins:
    wp.softPwmCreate(pin, 0, 100)  # Create PWM pin, initial value: 0, range: 0-100

def fade_leds():
    for duty_cycle in range(25, 101, 25):
        for pin in led_pins:
            wp.softPwmWrite(pin, duty_cycle)
        time.sleep(2)  # Time between steps

# Fade the LEDs
try:
    while True:
        fade_leds()
except KeyboardInterrupt:
    # Clean up GPIO on exit
    for pin in led_pins:
        wp.softPwmWrite(pin, 0)
    print("\nProgram interrupted.")
