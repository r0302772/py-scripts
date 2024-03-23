import wiringpi
import time

def ActivateADC ():
    wiringpi.digitalWrite(pin_CS_adc, 0)       # Actived ADC using CS
    time.sleep(0.000005)

def DeactivateADC():
    wiringpi.digitalWrite(pin_CS_adc, 1)       # Deactived ADC using CS
    time.sleep(0.000005)

def readadc(adcnum): 
    if ((adcnum > 7) or (adcnum < 0)): 
        return -1 
    revlen, recvData = wiringpi.wiringPiSPIDataRW(1, bytes([1,(8+adcnum)<<4,0]))
    time.sleep(0.000005)
    adcout = ((recvData[1]&3) << 8) + recvData[2] 
    return adcout

# Set GPIO pins
LED_PIN_A = 1
LED_PIN_B = 2
pin_CS_adc = 16 # We will use w16 as CE, not the default pin w15!

# Define the hysteresis gap
hysteresis_gap = 10  # Adjust this value as needed

# Setup
wiringpi.wiringPiSetup() 
wiringpi.pinMode(pin_CS_adc, 1)                 # Set ce to mode 1 ( OUTPUT )
wiringpi.wiringPiSPISetupMode(1, 0, 500000, 0)  #(channel, port, speed, mode)

wiringpi.pinMode(LED_PIN_A, wiringpi.OUTPUT)
wiringpi.pinMode(LED_PIN_B, wiringpi.OUTPUT)

# Main
try:
    while True:
        ActivateADC()
        tmp0 = readadc(0) # read channel 0
        DeactivateADC()
        ActivateADC()
        tmp1 = readadc(1) # read channel 1
        DeactivateADC()
        print ("input0:",tmp0)
        print ("input1:",tmp1)

        # Control the LEDs based on the voltage of tmp0 and tmp1 with a hysteresis gap
        if tmp0 > tmp1 + hysteresis_gap:
            wiringpi.digitalWrite(LED_PIN_A, wiringpi.HIGH) # Turn ON LED A
            wiringpi.digitalWrite(LED_PIN_B, wiringpi.LOW)  # Turn OFF LED B
        elif tmp1 > tmp0 + hysteresis_gap:
            wiringpi.digitalWrite(LED_PIN_B, wiringpi.HIGH) # Turn ON LED B
            wiringpi.digitalWrite(LED_PIN_A, wiringpi.LOW)  # Turn OFF LED A

        time.sleep(0.2)

except KeyboardInterrupt:
    DeactivateADC()
    wiringpi.digitalWrite(LED_PIN_A, wiringpi.LOW)  # Turn OFF LED A
    wiringpi.digitalWrite(LED_PIN_B, wiringpi.LOW)  # Turn OFF LED B
    print("\nProgram terminated")
