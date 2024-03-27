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

# Setup
pin_CS_adc = 16  # We will use w16 as CE, not the default pin w15!
pin_led_1 = 2  # Pin for first LED
pin_led_2 = 3  # Pin for second LED
min_brightness = 20  # Set minimum brightness value
wiringpi.wiringPiSetup()
wiringpi.pinMode(pin_CS_adc, 1)  # Set ce to mode 1 ( OUTPUT )
wiringpi.pinMode(pin_led_2, 1)  # Set pin3 to mode 1 ( OUTPUT )
wiringpi.wiringPiSPISetupMode(1, 0, 500000, 0)  # (channel, port, speed, mode)
wiringpi.softPwmCreate(pin_led_1, 0, 100)  # Set pin2 as a softPWM output

# Main
try:
    while True:
        ActivateADC()
        tmp0 = readadc(0)  # read channel 0
        DeactivateADC()
        print ("input0:",tmp0)
        controlLEDs(pin_led_1, pin_led_2, tmp0 // 10, min_brightness)  # Control LED brightness based on potentiometer
        time.sleep(0.2)

except KeyboardInterrupt:
    wiringpi.softPwmWrite(pin_led_1, 0)  # stop the PWM output
    wiringpi.digitalWrite(pin_led_2, 0)  # Turn off the second LED
    DeactivateADC()
    print("\nProgram terminated")
