import wiringpi
import time

# Functions for ADC
def ActivateADC():
    wiringpi.digitalWrite(pin_CS_adc, 0)  # Activate ADC using CS
    time.sleep(0.000005)

def DeactivateADC():
    wiringpi.digitalWrite(pin_CS_adc, 1)  # Deactivate ADC using CS
    time.sleep(0.000005)

def readadc(adcnum):
    if ((adcnum > 7) or (adcnum < 0)):
        return -1
    revlen, recvData = wiringpi.wiringPiSPIDataRW(1, bytes([1, (8 + adcnum) << 4, 0]))
    time.sleep(0.000005)
    adcout = ((recvData[1] & 3) << 8) + recvData[2]
    return adcout

# Function for LED control
def controlLEDs(sig1, sig2, cnt, min_brightness):
    wiringpi.softPwmWrite(sig1, cnt)
    if cnt < min_brightness:
        wiringpi.digitalWrite(sig2, not wiringpi.digitalRead(sig2))  # Toggle the second LED
        time.sleep(0.1)  # Control the flash rate
    else:
        wiringpi.digitalWrite(sig2, 0)  # Turn off the second LED

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

# Setup
pin_CS_adc = 16  # We will use w16 as CE, not the default pin w15!
pin_led_1 = 2  # Pin for first LED
pin_led_2 = 3  # Pin for second LED
pin_led_rgb_red = 10
pin_led_rgb_blue = 6
TRIGGER_PIN = 1  # Output pin for ultrasonic sensor
ECHO_PIN = 4     # Input pin for ultrasonic sensor
min_brightness = 20  # Set minimum brightness value
wiringpi.wiringPiSetup()
wiringpi.pinMode(pin_CS_adc, 1)  # Set ce to mode 1 ( OUTPUT )
wiringpi.pinMode(pin_led_2, 1)  # Set pin3 to mode 1 ( OUTPUT )
wiringpi.pinMode(TRIGGER_PIN, wiringpi.OUTPUT)
wiringpi.pinMode(ECHO_PIN, wiringpi.INPUT)
wiringpi.wiringPiSPISetupMode(1, 0, 500000, 0)  # (channel, port, speed, mode)
wiringpi.softPwmCreate(pin_led_1, 0, 100)  # Set pin2 as a softPWM output
wiringpi.pinMode(pin_led_rgb_red, 1)  # Set pin10 to mode 1 ( OUTPUT )
wiringpi.pinMode(pin_led_rgb_blue, 1)  # Set pin6 to mode 1 ( OUTPUT )

# Main
try:
    while True:
        ActivateADC()
        tmp0 = readadc(0)  # read channel 0
        DeactivateADC()
        print ("input0:",tmp0)
        controlLEDs(pin_led_1, pin_led_2, tmp0 // 10, min_brightness)  # Control LED brightness based on potentiometer
        distance = measure_distance()
        print(f"Measured Distance = {round(distance, 2)} cm")
        if distance < 50:
            wiringpi.digitalWrite(pin_led_rgb_red, 1)  # Turn on the red LED
        else:
            wiringpi.digitalWrite(pin_led_rgb_red, 0)  # Turn off the red LED
        if 50 <= distance <= 80:
            wiringpi.digitalWrite(pin_led_rgb_blue, 1)  # Turn on the blue LED
        else:
            wiringpi.digitalWrite(pin_led_rgb_blue, 0)  # Turn off the blue LED
        time.sleep(0.2)

except KeyboardInterrupt:
    wiringpi.softPwmWrite(pin_led_1, 0)  # stop the PWM output
    wiringpi.digitalWrite(pin_led_2, 0)  # Turn off the second LED
    wiringpi.digitalWrite(pin_led_rgb_red, 0)  # Turn off the red LED
    wiringpi.digitalWrite(pin_led_rgb_blue, 0)  # Turn off the blue LED
    DeactivateADC()
    print("\nProgram terminated")
