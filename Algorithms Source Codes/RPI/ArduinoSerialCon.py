# -*- coding: utf-8 -*-
"""
Created on Wed Sep 28 14:17:53 2016

@author: lwh92
"""
import serial
import threading
import time

class ArduinoSerialCon(object):
    def __init__(self):
        self.bufFile = '/dev/ttyACM0'
        self.baudRate = 115200
        self.serConn = None

    def connect(self):
        self.serConn = serial.Serial(self.bufFile,self.baudRate)
        self.serConn.flush()
    
    def readArduino(self):
        print "Trying to connect to arduino"
        while self.serConn == None: 
            self.connect()
        print "Starting to read"
        print self.serConn
        try:
            data = self.serConn.readline()
            # delay between write and read
            time.sleep(.2)
            print ("From Arduino: " + data)
            return data
        except Exception, e:
            print ("Fail to read from Arduino")
            print e
                
    def writeArduino(self,inData):
        print "Trying to connect to arduino"
        while self.serConn == None: 
            self.connect()
        print "Starting to write"
        print self.serConn
        try:
            self.serConn.write(inData)
            # delay between write and read
            time.sleep(.2)
            print ("To Arduino: " + inData)
        except Exception, e:
            print ("Fail to write to Arduino")

    def close(self):
        self.serConn.close()
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
