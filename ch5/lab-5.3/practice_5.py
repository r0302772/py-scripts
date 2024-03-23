import wiringpi
import time

# Define GPIO pins for ultrasonic sensor
TRIGGER_PIN = 1  # Output pin
ECHO_PIN = 2     # Input pin

# Initialize WiringPi
wiringpi.wiringPiSetup()

# Set GPIO pin modes
wiringpi.pinMode(TRIGGER_PIN, wiringpi.OUTPUT)
wiringpi.pinMode(ECHO_PIN, wiringpi.INPUT)

# Function to measure distance
def measure_distance():
    # Send ultrasonic pulse
    wiringpi.digitalWrite(TRIGGER_PIN, wiringpi.HIGH)
    time.sleep(0.00001)  # 10 microseconds
    wiringpi.digitalWrite(TRIGGER_PIN, wiringpi.LOW)

    # Wait for the pulse to return
    while wiringpi.digitalRead(ECHO_PIN) == wiringpi.LOW:
        signal_high = time.time()

    while wiringpi.digitalRead(ECHO_PIN) == wiringpi.HIGH:
        signal_low = time.time()

    # Calculate time passed
    time_passed = signal_low - signal_high

    # Calculate distance in centimeters
    distance = time_passed * 17000

    return distance

# Main program
try:
    while True:
        distance = measure_distance()
        print(f"Measured Distance = {round(distance, 2)} cm")
        time.sleep(0.1)  # Adjust interval as needed
except KeyboardInterrupt:
    print("\nProgram terminated.")
