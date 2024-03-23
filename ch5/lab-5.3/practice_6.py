import wiringpi
import time

# Define GPIO pins for ultrasonic sensor, LED
TRIGGER_PIN = 1  # Output pin for ultrasonic sensor
ECHO_PIN = 2     # Input pin for ultrasonic sensor
LED_PIN = 3      # Output pin for LED

# Stepper motor
IN1 = 13  # Connect OrangePi pin w13 to IN1
IN2 = 14  # Connect OrangePi pin w14 to IN2
IN3 = 15  # Connect OrangePi pin w15 to IN3
IN4 = 16  # Connect OrangePi pin w16 to IN4

# Define the delay between steps
step_delay = 0.1 # 10ms
# step_delay = 1 # 1000ms

# Initialize WiringPi
wiringpi.wiringPiSetup()

# Set GPIO pin modes
wiringpi.pinMode(ECHO_PIN, wiringpi.INPUT)

for pin in [TRIGGER_PIN, LED_PIN, IN1, IN2, IN3, IN4]:
    wiringpi.pinMode(pin, wiringpi.OUTPUT)

# Define step sequences for Wave drive
wave_drive_sequence = [
    [1, 0, 0, 0],
    [0, 1, 0, 0],
    [0, 0, 1, 0],
    [0, 0, 0, 1]
]

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

# Function to rotate the motor in the specified mode and direction
def rotate_motor(direction):
    for half_step in wave_drive_sequence if direction == "CW" else reversed(wave_drive_sequence):
        for i, pin in enumerate([IN1, IN2, IN3, IN4]):
            wiringpi.digitalWrite(pin, half_step[i])
        time.sleep(step_delay)

# Function to stop the motor
def stop_motor():
    for pin in [IN1, IN2, IN3, IN4]:
        wiringpi.digitalWrite(pin, 0)  # Turn off all motor pins

# Function to control LED and stepper motor
def control_devices(distance):
    if distance < 30:
        print(f"Alarm: {round(distance, 2)} cm")
        wiringpi.digitalWrite(LED_PIN, wiringpi.HIGH)  # Turn on LED
        rotate_motor(direction="CW")  # Rotate motor
    else:
        print(f"Safe: {round(distance, 2)} cm")
        wiringpi.digitalWrite(LED_PIN, wiringpi.LOW)  # Turn off LED
        stop_motor()  # Stop motor

# Main program
try:
    while True:
        distance = measure_distance()
        control_devices(distance)
        time.sleep(0.1)  # Adjust interval as needed
except KeyboardInterrupt:
    print("\nProgram terminated.")
