import serial
import threading
import time

class ArduinoSerialCon(object):
    def __init__(self):
        self.bufFile = '/dev/ttyACM1'
        self.bufFile2 = '/dev/ttyACM1'
        self.baudRate = 115200
        self.serConn = None

    def connect(self):
        self.serConn = serial.Serial(self.bufFile,self.baudRate)
        self.serConn.flush()
    
    def readArduino(self):
        while self.serConn == None: 
            self.connect()
        try:
            data = self.serConn.readline()
            return data
        except Exception, e:
            print ("Fail to read from Arduino")
            print e
                
    def writeArduino(self, inData):
        while self.serConn == None: 
            self.connect()
        try:
            self.serConn.write(inData)
        except Exception, e:
            print ("Fail to write to Arduino")

    def close(self):
        self.serConn.close()

