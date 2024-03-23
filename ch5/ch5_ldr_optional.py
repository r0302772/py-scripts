import wiringpi
import time

# Define GPIO pin for LDR input
LDR_PIN = 1

# Initialize WiringPi
wiringpi.wiringPiSetup()

# Function to measure light intensity
def measure_light():
    # Step 1: Set GPIO pin as output and drive it low
    wiringpi.pinMode(LDR_PIN, wiringpi.OUTPUT)
    wiringpi.digitalWrite(LDR_PIN, wiringpi.LOW)
    time.sleep(0.1)  # Time to discharge the capacitor

    # Step 2: Set GPIO pin as input to start charging the capacitor
    wiringpi.pinMode(LDR_PIN, wiringpi.INPUT)
    
    # Step 3: Measure the time until the input goes high
    start_time = time.time()
    while wiringpi.digitalRead(LDR_PIN) == wiringpi.LOW:
        pass
    stop_time = time.time()
    
    # Step 4: Calculate the interval and round it to the nearest integer
    interval = round((stop_time - start_time) * 1000000)  # Convert to milliseconds and round
    return int(interval)

# Main program
try:
    while True:
        light_interval = measure_light()
        print("Light intensity:", light_interval)
        time.sleep(0.5)  # Adjust interval as required
except KeyboardInterrupt:
    print("\nProgram terminated.")
