import wiringpi
import time

# Define the pins connected to the ULN2003 driver (IN1 - IN4)
IN1 = 16  # Connect OrangePi pin w16 to IN1
IN2 = 15  # Connect OrangePi pin w15 to IN2
IN3 = 14  # Connect OrangePi pin w14 to IN3
IN4 = 13  # Connect OrangePi pin w13 to IN4

# Define the GPIO pin for the push button
BUTTON = 2  # Connect OrangePi pin w2 to the button

# Define the delay between steps
step_delay = 0.1 # 10ms
# step_delay = 1 # 1000ms

# Initialize WiringPi
wiringpi.wiringPiSetup()

# Set all pins to output mode
for pin in [IN1, IN2, IN3, IN4]:
    wiringpi.pinMode(pin, wiringpi.OUTPUT)

# Set the button pin to input mode
wiringpi.pinMode(BUTTON, wiringpi.INPUT)

# Define step sequences for Full step
wave_drive_sequence = [
    [1, 0, 0, 0],
    [0, 1, 0, 0],
    [0, 0, 1, 0],
    [0, 0, 0, 1]
]

# Function to rotate the motor in the specified mode and direction
def rotate_motor(steps):
    for step in range(steps):
        # Check the state of the button in each step
        if wiringpi.digitalRead(BUTTON) == wiringpi.HIGH:
            # If the button is pressed, rotate CW
            rotation = "CW"
            half_step_sequence = wave_drive_sequence
        else:
            # If the button is not pressed, rotate CCW
            rotation = "CCW"
            half_step_sequence = reversed(wave_drive_sequence)
        
        for half_step in half_step_sequence:
            for i, pin in enumerate([IN1, IN2, IN3, IN4]):
                wiringpi.digitalWrite(pin, half_step[i])
            time.sleep(step_delay)
        print("Step: ", step, rotation)


# Main program
try:
    while True:
        print("Start")
        # Rotate motor
        rotate_motor(steps=2038)

except KeyboardInterrupt:
    # Clean up GPIO on exit
    for pin in [IN1, IN2, IN3, IN4]:
        wiringpi.digitalWrite(pin, wiringpi.LOW)
    print("\nProgram terminated.")

