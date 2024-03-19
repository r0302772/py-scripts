import time
import wiringpi

# SETUP
print("Start")
pin_relay_1 = 15
pin_relay_2 = 16
pin_switch_1 = 1
pin_switch_2 = 2
wiringpi.wiringPiSetup() 
wiringpi.pinMode(pin_relay_1, 1)       # Set pin to mode 1 (OUTPUT) for relay 1
wiringpi.pinMode(pin_relay_2, 1)       # Set pin to mode 1 (OUTPUT) for relay 2
wiringpi.pinMode(pin_switch_1, 0)    # Set pin to mode 0 (INPUT) for switch 1
wiringpi.pinMode(pin_switch_2, 0)    # Set pin to mode 0 (INPUT) for switch 2

# Function to switch the relay
def switch_relay(pin):
    wiringpi.digitalWrite(pin, 1)    # Turn on relay
    time.sleep(0.2)                  # Adjust delay for desired duration
    wiringpi.digitalWrite(pin, 0)    # Turn off relay

# Infinite loop - stop using CTRL-C
# Main program
try:
    while True:
        if wiringpi.digitalRead(pin_switch_2) == 0:  # If GPIO2 is activated
            switch_relay(pin_relay_1)  # Switch relay 1
        if wiringpi.digitalRead(pin_switch_1) == 0:  # If GPIO1 is activated
            switch_relay(pin_relay_2)  # Switch relay 2
        time.sleep(0.5)  # Add a small delay to avoid high CPU usage
except KeyboardInterrupt:
    print("\nProgram terminated.")
