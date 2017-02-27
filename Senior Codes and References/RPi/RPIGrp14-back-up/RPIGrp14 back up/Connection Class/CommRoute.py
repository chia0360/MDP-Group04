# -*- coding: utf-8 -*-
"""
Created on Fri Sep 30 10:08:34 2016

@author: lwh92
"""
import sys
import time
import Queue
from AndroidBTCon import *
from ArduinoSerialCon import *
from PCInetCon import *
import threading

arduino = ArduinoSerialCon()

bluetooth = AndroidBTCon()
bluetooth.connectBluetooth()

pc = PCInetCon()
pc.connectPc()

arduinoWrite = ArduinoSerialCon()

def routeFromPc():
    while 1:
        inData = pc.receivePc()
        print(inData)
        if (inData[0] == 'T'):
            bluetooth.writeBluetooth(inData[1:])
            print("Send to bluetooth : "+ inData[1:])
        elif (inData[0] == 'A'):
            arduino.writeArduino(inData[1:])
            print("Send to arduino : " + inData[1:])
        else:
            print("Route Command not found")
        
        
def routeToPc():
    while 1:
        ardData = arduino.readArduino()
        print ("Back to PC "+ ardData)
        pc.sendPc(ardData)


def btRouteToPc():
    while 1:
        btData = bluetooth.readBluetooth()
        print("Bluetooth data :" + btData)
        pc.sendPc("T"+btData)
        bluetooth.writeBluetooth(btData[1:])
    
    
t1 = threading.Thread(target=routeToPc, args=())
t1.daemon = True
t1.start()

t2 = threading.Thread(target=routeFromPc, args=())
t2.daemon = True
t2.start()

t3 = threading.Thread(target=btRouteToPc, args=())
t3.daemon = True
t3.start()
