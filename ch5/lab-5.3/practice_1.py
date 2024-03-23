import wiringpi
import time

# Define GPIO pin for LDR input
LDR_PIN = 1

# Initialize WiringPi
wiringpi.wiringPiSetup()

# Set GPIO pin as input
wiringpi.pinMode(LDR_PIN, wiringpi.INPUT)

# Function to check LDR status and print result
def check_ldr_status():
    if wiringpi.digitalRead(LDR_PIN) == wiringpi.LOW:
        print("Dark")
    else:
        print("Light")

# Main program
try:
    while True:
        check_ldr_status()
        time.sleep(0.5)  # Wait for 0.5 seconds
except KeyboardInterrupt:
    print("\nProgram terminated.")
