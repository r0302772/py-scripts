import time
import wiringpi

def blink(_pin):
    wiringpi.digitalWrite(_pin, 1)    # Write 1 ( HIGH ) to pin
    time.sleep(0.5)
    wiringpi.digitalWrite(_pin, 0)    # Write 1 ( HIGH ) to pin
    time.sleep(0.5)


# SETUP
print("Start")
pin = 2
wiringpi.wiringPiSetup() 
wiringpi.pinMode(pin, 1)            # Set pin to mode 1 ( OUTPUT )

# MAIN
try:
    while True:
        blink(pin)
except KeyboardInterrupt:
    # Clean up GPIO on exit
    wiringpi.digitalWrite(pin, 0)
    print("\nDone")