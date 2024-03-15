import time
import wiringpi

# SETUP
print("Start")
pin_led = 2
pin_switch = 1
wiringpi.wiringPiSetup() 
wiringpi.pinMode(pin_led, 1)       # Set pin to mode 1 (OUTPUT) for LED
wiringpi.pinMode(pin_switch, 0)    # Set pin to mode 0 (INPUT) for switch

# Function to blink the LED
def blink_led():
    wiringpi.digitalWrite(pin_led, 1)  # Turn on LED
    time.sleep(0.2)
    wiringpi.digitalWrite(pin_led, 0)  # Turn off LED
    time.sleep(0.2)

# Infinite loop - stop using CTRL-C
# Main program
try:
    while True:
        if wiringpi.digitalRead(pin_switch) == 0:  # Input is active low
            print("Button Pressed")
            time.sleep(0.3)  # Anti-bouncing
            while wiringpi.digitalRead(pin_switch) == 0:  # Wait until button released
                print("LED blinks")
                blink_led()  # Blink LED while button is pressed
        else:
            print("Button released")
            time.sleep(0.3)  # Anti-bouncing
            print("LED not flashing")
            wiringpi.digitalWrite(pin_led, 0)  # Turn off LED if button released
        time.sleep(0.5)  # Add a small delay to avoid high CPU usage
except KeyboardInterrupt:
    print("\nProgram terminated.")
