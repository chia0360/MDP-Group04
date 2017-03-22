import serial
import threading
import time

class ArduinoConnection(object):
    def __init__(self):
        self.bufFile = '/dev/ttyACM0'
        self.baudRate = 115200
        self.serConn = None

    def connect(self):
        self.serConn = serial.Serial(self.bufFile,self.baudRate)
        self.serConn.flush()
        print "Connected to arduino"
    
    def readMsg(self):
        while self.serConn == None: 
            self.connect()
        try:
            data = self.serConn.readline()
            return data
        except Exception, e:
            print "Error reading from arduino", str(e)
                
    def sendMsg(self, msg):
        while self.serConn == None: 
            self.connect()
        try:
            self.serConn.write(msg)
        except Exception, e:
            print "Error writing to arduino", str(e)

    def disconnect(self):
        self.serConn.close()
        print "Arduino Disconnected"

