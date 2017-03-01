import serial
import threading

class ArduinoSerialCon(object):
    def __init__(self):
        self.bufFile = '/dev/ttyACM0'
        self.baudRate = 9600
        self.serConn = None

    def connect(self):
        serial.Serial(self.bufFile,self.baudRate)
        try:
            self.serConn = serial.Serial(self.bufFile, self.baudRate)
            print ("Serial link connected")
        except Exception as e:
            print ("\nError (Serial): %s " % str(e))

    def readArduino(self):
        try:
            data = self.serConn.readline()
            print ("From Arduino: " + data)
            return data
        except Exception as e:
            self.connect()
            print ("Fail to read from Arduino")
            print (e)
                
    def writeArduino(self,inData):
        try:
            self.serConn.write(inData)
            print ("To Arduino: " + inData)
        except Exception as e:
            self.connect()
            print ("Fail to write to Arduino")
