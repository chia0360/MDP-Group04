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
        print("readArduino")
        while self.serConn == None: 
            self.connect()
        try:
            data = self.serConn.readline()
            # delay between write and read
            time.sleep(.05)
            print ("From Arduino: " + data)
            return data
        except Exception, e:
            print ("Fail to read from Arduino")
            print e
                
    def writeArduino(self, inData):
        while self.serConn == None: 
            self.connect()
        try:
            self.serConn.write(inData)
            # delay between write and read
            time.sleep(.05)
            print ("To Arduino: " + inData)
        except Exception, e:
            print ("Fail to write to Arduino")

    def close(self):
        self.serConn.close()