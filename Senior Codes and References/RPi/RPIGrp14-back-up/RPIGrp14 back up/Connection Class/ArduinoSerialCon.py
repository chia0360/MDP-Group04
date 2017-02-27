# -*- coding: utf-8 -*-
"""
Created on Wed Sep 28 14:17:53 2016

@author: lwh92
"""
import serial
import threading

class ArduinoSerialCon(object):
    def __init__(self):
        self.bufFile = '/dev/ttyACM0'
        self.baudRate = 9600
        self.serConn = serial.Serial(self.bufFile,self.baudRate)
        self.serConn.flush()
        
    def readArduino(self):
        try:
            data = self.serConn.readline()
            print ("From Arduino: " + data)
            return data
        except Exception, e:
                print ("Fail to read from Arduino")
                print e
                
    def writeArduino(self,inData):
        try:
            self.serConn.write(inData)
            print ("To Arduino: " + inData)
        except Exception, e:
            print ("Fail to write to Arduino")
"""

SC = ArduinoSerialCon()
   
def readArduino():
    while 1: 
        data = SC.readArduino()
        print ("From Arduino: " + data)
        
t1 = threading.Thread(target=readArduino, args=())
t1.start()

message = 'A'
while message != "END":
    message = raw_input("Input a char : ")
    SC.writeArduino(message)
    
"""
