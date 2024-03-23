import wiringpi
import time

# Setup
pin_CS_adc = 16                                 # We will use w16 as CE, not the default pin w15!
wiringpi.wiringPiSetup() 
wiringpi.pinMode(pin_CS_adc, 1)                 # Set ce to mode 1 ( OUTPUT )
wiringpi.wiringPiSPISetupMode(1, 0, 500000, 0)  #(channel, port, speed, mode)

def ActivateADC():
    wiringpi.digitalWrite(pin_CS_adc, 0)       # Activate ADC using CS
    time.sleep(0.000005)

def DeactivateADC():
    wiringpi.digitalWrite(pin_CS_adc, 1)       # Deactivate ADC using CS
    time.sleep(0.000005)

def readadc(adcnum): 
    if ((adcnum > 7) or (adcnum < 0)): 
        return -1 
    revlen, recvData = wiringpi.wiringPiSPIDataRW(1, bytes([1,(8+adcnum)<<4,0]))
    time.sleep(0.000005)
    adcout = ((recvData[1]&3) << 8) + recvData[2] 
    return adcout  

# Main loop
try:
    while True:
        ActivateADC()
        voltage = readadc(0) * 3.3 / 1023  # Read voltage from channel 0
        temperature = voltage * 100  # Convert voltage to temperature
        DeactivateADC()
        print ("Temperature:", round(temperature, 1), "°C")
        time.sleep(0.2)

except KeyboardInterrupt:
    DeactivateADC()
    print("\nProgram terminated")
