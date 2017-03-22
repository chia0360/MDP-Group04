
import threading
import socket
import time

class PCConnection(object):
    def __init__(self):
        self.port = 8888
        self.host = "192.168.4.1"
        self.socket = None
        self.client = None
        self.address = None

    def connect(self):
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.bind((self.host, self.port))
            self.socket.listen(5)
            print "Waiting for connection from PC..."
            self.client, self.address = self.socket.accept()
            print "Connected to: ", self.address
            return True
        except Exception, e:
            print "PC Connection Error", str(e)
            self.socket.close()
            if self.client is not None:
                self.client.close()

    def sendMsg(self,msg):
        try:
            self.client.send(msg)
        except Exception, e:
            print "Error writing to PC", str(e)
            self.connect()

    def readMsg(self):
        try:
            message = self.client.recv(1024)
            return message
        except Exception, e:
            print "Error reading from PC", str(e)
            self.connect()
      
    def disconnect(self):
        if self.socket:
            self.socket.close()
        if self.client:
            self.client.close()
        print "PC Disconnected"
