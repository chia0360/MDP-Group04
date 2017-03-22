
import threading
import socket
import time

class AndroidConnection(object):
    def __init__(self):
        self.port = 8765
        self.host = "192.168.4.1"
        self.socket = None
        self.client = None
        self.address = None

    def connect(self):
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.bind((self.host, self.port))
            self.socket.listen(5)
            print "Waiting for connection from Android..."
            self.client, self.address = self.socket.accept()
            print "Connected to: ", self.address
            return True
        except Exception, e:
            print "Android Connection Error", str(e)
            self.socket.close()
            if self.client is not None:
                self.client.close()

    def sendMsg(self,msg):
        try:
            self.client.send(msg)
	except Exception, e:
            print "Error writing to android", str(e)
            self.connect()

    def readMsg(self):
        try:
            message = self.client.recv(1024)
            return message[:-1]
        except Exception, e:
            print "Error reading from android", str(e)
            self.connect()
      
    def disconnect(self):
        if self.socket:
            self.socket.close()
        if self.client:
            self.client.close()
        print "Android Disconnected"
