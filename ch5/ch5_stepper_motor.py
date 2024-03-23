import wiringpi
import time

# Define the pins connected to the ULN2003 driver (IN1 - IN4)
IN1 = 3  # Connect OrangePi pin w3 to IN1
IN2 = 4  # Connect OrangePi pin w4 to IN2
IN3 = 6  # Connect OrangePi pin w6 to IN3
IN4 = 9  # Connect OrangePi pin w9 to IN4

# Define the delay between steps (10ms)
step_delay = 0.1

# Initialize WiringPi
wiringpi.wiringPiSetup()

# Set all pins to output mode
for pin in [IN1, IN2, IN3, IN4]:
    wiringpi.pinMode(pin, wiringpi.OUTPUT)

# Define step sequences for Wave drive and Full step
wave_drive_sequence = [
    [1, 0, 0, 0],
    [0, 1, 0, 0],
    [0, 0, 1, 0],
    [0, 0, 0, 1]
]

full_step_sequence = [
    [1, 0, 1, 0],
    [0, 1, 1, 0],
    [0, 1, 0, 1],
    [1, 0, 0, 1]
]

# Function to rotate the motor in the specified mode and direction
def rotate_motor(mode, direction, steps):
    sequence = wave_drive_sequence if mode == "Wave" else full_step_sequence

    for _ in range(steps):
        for half_step in sequence if direction == "CW" else reversed(sequence):
            for i, pin in enumerate([IN1, IN2, IN3, IN4]):
                wiringpi.digitalWrite(pin, half_step[i])
            time.sleep(step_delay)

# Main program
try:
    while True:
        # Rotate CW slowly in Wave drive mode
        rotate_motor(mode="Wave", direction="CW", steps=2038)

        # Rotate CCW quickly in Full step mode
        rotate_motor(mode="Full", direction="CCW", steps=2038)

except KeyboardInterrupt:
    # Clean up GPIO on exit
    for pin in [IN1, IN2, IN3, IN4]:
        wiringpi.digitalWrite(pin, wiringpi.LOW)
    print("\nProgram terminated.")
