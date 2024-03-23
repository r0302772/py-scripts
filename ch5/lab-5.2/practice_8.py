import wiringpi
import time

# Define the pins connected to the ULN2003 driver (IN1 - IN4)
IN1 = 16  # Connect OrangePi pin w16 to IN1
IN2 = 15  # Connect OrangePi pin w15 to IN2
IN3 = 14  # Connect OrangePi pin w14 to IN3
IN4 = 13  # Connect OrangePi pin w13 to IN4

# Define the delay between steps
# step_delay = 0.1 # 10ms
step_delay = 1 # 1000ms

# Initialize WiringPi
wiringpi.wiringPiSetup()

# Set all pins to output mode
for pin in [IN1, IN2, IN3, IN4]:
    wiringpi.pinMode(pin, wiringpi.OUTPUT)

# Define step sequences for Full step
full_step_sequence = [
    [1, 0, 1, 0],
    [0, 1, 1, 0],
    [0, 1, 0, 1],
    [1, 0, 0, 1]
]

# Function to rotate the motor in the specified mode and direction
def rotate_motor(direction, steps):
    for _ in range(steps):
        for half_step in full_step_sequence if direction == "CW" else reversed(full_step_sequence):
            for i, pin in enumerate([IN1, IN2, IN3, IN4]):
                wiringpi.digitalWrite(pin, half_step[i])
            time.sleep(step_delay)

# Main program
try:
    while True:
        print("Start")
        # Rotate CW
        rotate_motor(direction="CW", steps=2038)
        # Rotate CCW
        rotate_motor(direction="CCW", steps=2038)

except KeyboardInterrupt:
    # Clean up GPIO on exit
    for pin in [IN1, IN2, IN3, IN4]:
        wiringpi.digitalWrite(pin, wiringpi.LOW)
    print("\nProgram terminated.")
