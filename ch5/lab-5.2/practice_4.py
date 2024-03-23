import wiringpi
import time

# SETUP
print("Start")
output_pin = 2
input_pin = 1
wiringpi.wiringPiSetup() 
wiringpi.pinMode(output_pin, 1)  # Set output_pin to mode 1 ( OUTPUT )
wiringpi.pinMode(input_pin, 0)   # Set input_pin to mode 0 ( INPUT )

# Define Morse code for SOS
SOS_MORSE_CODE = [".", ".", ".", "-", "-", "-", ".", ".", "."]
MORSE_UNIT_DURATION = 0.5  # Duration of one Morse code unit in seconds

# Function to blink Morse code
def blink_morse_code(pin, morse_code):
    for symbol in morse_code:
        if wiringpi.digitalRead(input_pin) == 1:  # If input GPIO2 is active, stop the SOS signal
            break
        if symbol == ".":
            wiringpi.digitalWrite(pin, 1)  # Short pulse (dot)
            time.sleep(MORSE_UNIT_DURATION)
        elif symbol == "-":
            wiringpi.digitalWrite(pin, 1)  # Long pulse (dash)
            time.sleep(MORSE_UNIT_DURATION * 3)  # Long pulse duration is 3 times that of short pulse
        wiringpi.digitalWrite(pin, 0)  # Turn off LED
        time.sleep(MORSE_UNIT_DURATION)  # Inter-element gap

# Main loop to repeat SOS signal
try:
    while True:
        blink_morse_code(output_pin, SOS_MORSE_CODE)
        if wiringpi.digitalRead(input_pin) == 1:  # If input GPIO2 is active, stop the SOS signal
            break
        time.sleep(3)  # Inter-word gap after each SOS sequence
except KeyboardInterrupt:
    # Clean up GPIO on exit
    wiringpi.digitalWrite(output_pin, 0)
    print("\nProgram terminated.")
