import wiringpi
import time

# SETUP
print("Start")
pin = 2
wiringpi.wiringPiSetup() 
wiringpi.pinMode(pin, 1)            # Set pin to mode 1 ( OUTPUT )

# Define Morse code for SOS
SOS_MORSE_CODE = [".", ".", ".", "-", "-", "-", ".", ".", "."]
MORSE_UNIT_DURATION = 0.5  # Duration of one Morse code unit in seconds

# Function to blink Morse code
def blink_morse_code(pin, morse_code):
    for symbol in morse_code:
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
        blink_morse_code(pin, SOS_MORSE_CODE)
        time.sleep(3)  # Inter-word gap after each SOS sequence
except KeyboardInterrupt:
    # Clean up GPIO on exit
    wiringpi.digitalWrite(pin, 0)
    print("\nDone")
