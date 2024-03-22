import wiringpi
import time

# Define GPIO pin for LDR, SWITCH input and LED output
LDR_PIN = 1
LED_PIN = 2
SWITCH_PIN = 11

# Initialize WiringPi
wiringpi.wiringPiSetup()

# Set GPIO pin as input and output
wiringpi.pinMode(LDR_PIN, wiringpi.INPUT)
wiringpi.pinMode(LED_PIN, wiringpi.OUTPUT)
wiringpi.pinMode(SWITCH_PIN, wiringpi.INPUT)

# Function to check LDR status and print result
def check_ldr_status():
    if wiringpi.digitalRead(LDR_PIN) == wiringpi.LOW or wiringpi.digitalRead(SWITCH_PIN) == wiringpi.LOW:
        print("Light on")
        wiringpi.digitalWrite(LED_PIN, wiringpi.HIGH)  # Turn on LED
    else:
        print("Light off")
        wiringpi.digitalWrite(LED_PIN, wiringpi.LOW)  # Turn off LED

# Main program
try:
    while True:
        check_ldr_status()
        time.sleep(0.5)  # Wait for 0.5 seconds
except KeyboardInterrupt:
    print("\nProgram terminated.")
