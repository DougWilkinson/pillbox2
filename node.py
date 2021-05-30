from sensorclass import Sensor
from machine import Pin
from neopixel import NeoPixel
import time

brightness = Sensor("brightness", "VS", initval=4)

# Neopixel, hallsensor, pill# status (needed or good)
pills = [[NeoPixel(Pin(4), 1),\
    Sensor("sensor0", "IN", 12, onname="off", offname="on"),\
    Sensor("pill0", "VS", initval="unknown" )],\
    [NeoPixel(Pin(5), 1),\
    Sensor("sensor1", "IN", 14, onname="off", offname="on"),\
    Sensor("pill1", "VS", initval="unknown" )]]

statusled = Sensor("led", "OUT", 2)
statusled.setstate(True)

medstatuslast = time.ticks_ms()

def showmedstatus():
    global medstatuslast
    pulse = time.ticks_ms() - medstatuslast
    if pulse > 500:
        pulse = 500
        medstatuslast = time.ticks_ms()
    pulse = abs(int(60 * (pulse/500)) - 30)
    for p in pills:
        p[0][0] = [16-(pulse >>1),0,pulse >> 1 ]
        if p[2].value == "good":
            p[0][0] = [0,2,0]
        if p[2].value == "needed":
            p[0][0] = [pulse,0,0]
        if p[1].value == "off":
            p[0][0] = [0,0,pulse >> 1]
    for p in pills:
        p[0].write()
        

# Called from main.py
def main():
    Sensor.MQTTSetup("pillbox")
    while True:
        Sensor.Spin()
        #Add actions here
        showmedstatus()
