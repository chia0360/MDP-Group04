
import threading
import socket
import time

class AndroidWifiCon(object):
    def __init__(self):
        self.port = 8765
        self.host = "192.168.4.1"
        self.socket = None
        self.client = None
        self.address = None

    def connectAndroid(self):
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.bind((self.host, self.port))
            self.socket.listen(5)
            print "Waiting for android incoming connection"
            self.client, self.address = self.socket.accept()
            print "Connected to: ", self.address
            return True
        except Exception, e:
            print "Fail to open socket connection", str(e)
            self.socket.close()
            if self.client is not None:
                self.client.close()

    def sendAndroid(self,outData):
        try:
            self.client.send(outData)
	except Exception, e:
            print "Fail to send data to android", str(e)
            self.connectAndroid()

    def receiveAndroid(self):
        try:
            message = self.client.recv(1024)
            return message[:-1]
        except Exception, e:
            print "Fail to receive data from android", str(e)
            self.connectAndroid()
      
    def disconnect(self):
        if self.socket:
            self.socket.close()
        if self.client:
            self.client.close()
        print "Disconnected"