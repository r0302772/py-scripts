import time
import threading
import wiringpi
from  ..ch7.ch7_ClassLCD import LCD

exit_event = threading.Event()

#global variables
adcValue = 0
timeStep = 0.002
motorDirection = "forward"

#setup
wiringpi.wiringPiSetup() 
wiringpi.wiringPiSPISetupMode(1, 0, 400000, 0)  #(channel, port, speed, mode)
pin_CS_lcd = 13
wiringpi.pinMode(pin_CS_lcd , 1)            # Set pin to mode 1 ( OUTPUT )
pin_CS_adc = 16                             # We will use w16 as CE, not the default pin w15!
wiringpi.pinMode(pin_CS_adc, 1)             # Set ce to mode 1 ( OUTPUT )

#stepper motor pins
pinList = [3, 4, 6, 0]
for pin in pinList:
    wiringpi.pinMode(pin, 1) #set motor pins as output

#lcd pins
PIN_OUT     =   {  
                'SCLK'  :   14,
                'DIN'   :   11,
                'DC'    :   9, 
                'CS'    :   15, # We will not connect this pin! --> we use w13
                'RST'   :   10,
                'LED'   :   6, #backlight   
}

def ActivateLCD():
    wiringpi.digitalWrite(pin_CS_lcd, 0)       # Actived LCD using CS
    time.sleep(0.000005)

def DeactivateLCD():
    wiringpi.digitalWrite(pin_CS_lcd, 1)       # Deactived LCD using CS
    time.sleep(0.000005)

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

def forward():
    for pin in pinList:
        wiringpi.digitalWrite(pin, 1)
        time.sleep(timeStep)
        wiringpi.digitalWrite(pin, 0)

def backward():
    for pin in pinList[::-1]:
        wiringpi.digitalWrite(pin, 1)
        time.sleep(timeStep)
        wiringpi.digitalWrite(pin, 0)

def motor():
    global motorDirection
    while True:
        if adcValue > 512:
            forward()
            motorDirection = "forward"
        else:
            backward()
            motorDirection = "backward"
        if exit_event.is_set():
            break

def lcd():
    while True:
        ActivateLCD()
        lcd_1.clear()
        lcd_1.go_to_xy(0, 0)
        lcd_1.put_string(str(adcValue))
        lcd_1.refresh()
        DeactivateLCD()
        time.sleep(1)
        if exit_event.is_set():
            break

def adc():
    global adcValue
    while True:
        ActivateADC()
        adcValue = readadc(0)
        DeactivateADC()
        time.sleep(1)
        if exit_event.is_set():
            break

#setup lcd
ActivateLCD()
lcd_1 = LCD(PIN_OUT)

#create new threads
t1 = threading.Thread(target=motor)
t2 = threading.Thread(target=lcd)
t3 = threading.Thread(target=adc)

#start the threads
t1.start()
t2.start()
t3.start()

#main function
try:
    while True:
        print(motorDirection, adcValue)
        time.sleep(1) 
except KeyboardInterrupt:
    exit_event.set()

