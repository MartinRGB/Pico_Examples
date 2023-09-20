#https://www.tomshardware.com/how-to/lcd-display-raspberry-pi-pico
from machine import I2C, Pin
from time import sleep
from pico_i2c_lcd import I2cLcd
from ds1302 import DS1302

i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000)

I2C_ADDR = i2c.scan()[0]
lcd = I2cLcd(i2c, I2C_ADDR, 2, 16)

led1=Pin(18,Pin.OUT)        #create LED object from pin13,Set Pin13 to output
led2=Pin(19,Pin.OUT)        #create LED object from pin13,Set Pin13 to output
led3=Pin(20,Pin.OUT)        #create LED object from pin13,Set Pin13 to output
ledText=['red','yellow','green']
ledArr=[led1,led2,led3]


ldr = machine.ADC(26)

sensor_temp = machine.ADC(4)
conversion_factor = 3.3 / (65535)

ds = DS1302(Pin(18),Pin(17),Pin(16))

ds.date_time() # returns the current datetime.

ds.date_time([2023, 9, 18, 0, 5, 33, 50, 0]) # set datetime.

while True:
    print(I2C_ADDR)
    lcd.blink_cursor_on()
    ledArr[0].value(0)
    ledArr[1].value(0)
    ledArr[2].value(0)
    lcd.putstr("I2C Address:"+str(I2C_ADDR)+"\n")
    sleep(2)
    lcd.clear()
    ledArr[0].value(1)
    ledArr[1].value(1)
    ledArr[2].value(1)
    lcd.putstr("Martin's Playin" +"\n")
    lcd.putstr("Pico")
    sleep(2)
    
    lcd.clear()
    ledArr[0].value(1)
    ledArr[1].value(0)
    ledArr[2].value(0)
    lcd.putstr("Light Perc is:" +"\n") 
    lcd.putstr(str(ldr.read_u16()/65536*100)[:4] +'%')
    sleep(2)
    
    lcd.clear()
    ledArr[0].value(0)
    ledArr[1].value(1)
    ledArr[2].value(0)
    reading = sensor_temp.read_u16() * conversion_factor 
    temperature = 27 - (reading - 0.706)/0.001721
    lcd.putstr("Temperature is:" +"\n") 
    lcd.putstr(str(temperature)[:4])
    sleep(2)
    
    lcd.clear()
    ledArr[0].value(0)
    ledArr[1].value(0)
    ledArr[2].value(1)
    (Y,M,D,day,hr,m,s)=ds.date_time()
    if s < 10:
        s = "0" + str(s)
    if m < 10:
        m = "0" + str(m)
    if hr < 10:
        hr = "0" + str(hr)
    if D < 10:
        D = "0" + str(D)
    if M < 10:
        M = "0" + str(M)
        
    lcd.move_to(0,0)
    lcd.putstr("Time:")
    lcd.move_to(6,0)
    lcd.putstr(str(hr) + ":" + str(m) + ":" + str(s))
    lcd.move_to(0,1)
    lcd.putstr("Date:")
    lcd.move_to(6,1)
    lcd.putstr(str(D) + "/" + str(M) + "/" + str(Y))
    sleep(2)
    
    lcd.blink_cursor_off()
    lcd.clear()
    
    
    lcd.putstr("Backlight Test")
    for i in range(10):
        lcd.backlight_on()
        ledArr[0].value(1)
        ledArr[1].value(1)
        ledArr[2].value(1)
        sleep(0.2)
        lcd.backlight_off()
        ledArr[0].value(0)
        ledArr[1].value(0)
        ledArr[2].value(0)
        sleep(0.2)
    lcd.backlight_on()
    lcd.hide_cursor()
    lcd.clear()
    for i in range(12):
        ledArr[0].value(0)
        ledArr[1].value(0)
        ledArr[2].value(0)
        lcd.putstr(str(i) + ': ' + ledText[i%3])
        ledArr[i%3].value(1)
        sleep(0.4)
        lcd.clear()
