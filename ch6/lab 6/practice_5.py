import wiringpi
import time
import json
import requests

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

#Setup
pin_CS_adc = 16                                 #We will use w16 as CE, not the default pin w15!
wiringpi.wiringPiSetup() 
wiringpi.pinMode(pin_CS_adc, 1)                 # Set ce to mode 1 ( OUTPUT )
wiringpi.wiringPiSPISetupMode(1, 0, 500000, 0)  #(channel, port, speed, mode)
url = "http://3wtiotessentials.hub.ubeac.io/iotessdennisnijs"
uid = "iotessdennisnijs"

# Main loop
try:
    while True:
        ActivateADC()
        voltage = readadc(0) * 3.3 / 1023  # Read voltage from channel 0
        temperature = voltage * 100  # Convert voltage to temperature
        tmp0 = round(temperature, 1)
        DeactivateADC()
        ActivateADC()
        light_intensity = readadc(1)  # Read light intensity from channel 1
        light_percentage = (light_intensity / 1023) * 100  # Convert to percentage
        tmp1 = round(light_percentage, 1)
        DeactivateADC()
        data= {
            "id": uid,
            "sensors":[{
                'id': 'adc ch0 - Temperature',
                'data': tmp0
                 },
                 {'id': 'adc ch1 - Light Intensity',
                 'data': tmp1
                }]
            }

        r = requests.post(url, verify=False, json=data)
        print ("Temperature:", round(temperature, 1), "°C")
        print ("Light Intensity:", round(light_percentage, 1), "%")
        time.sleep(1)

except KeyboardInterrupt:
    DeactivateADC()
    print("\nProgram terminated")