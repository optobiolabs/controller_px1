#!/usr/local/bin/python2

import serial
import serial.tools.list_ports as list_ports
#import time

# Wait for 5 seconds


cdc = list(list_ports.grep("41"))

if cdc:
    arduino = serial.Serial(cdc[0][0], 115200)
    #time.sleep(5)
else:
    class arduino:
        name = 'no device found'


#print(arduino.name)
