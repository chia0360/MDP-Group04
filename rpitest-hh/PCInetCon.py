
import threading
import socket
import time

class PCInetCon(object):
    def __init__(self):
        self.port = 8888
        self.host = "192.168.1.4"
        self.socket = None
        self.client = None
        self.address = None

    def connectPc(self):
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.bind((self.host, self.port))
            self.socket.listen(5)
            print "Waiting for PC incomming connection"
            self.client, self.address = self.socket.accept()
            print "Connected to: ", self.address
            return True
        except Exception, e:
            print "Fail to open socket connection", str(e)
            self.socket.close()
            if self.client is not None:
                self.client.close()

    def sendPc(self,outData):
        time.sleep(.05)
        
        try:
            self.client.send(outData)
        except Exception, e:
            print "Fail to send data", str(e)
            self.connectPc()

    def receivePc(self):
        time.sleep(.05)
        try:
            message = self.client.recv(1024)
            print("receivePC", message)
            return message
        except Exception, e:
            print "Fail to receive data", str(e)
            self.connectPc()
      
    def disconnect(self):
        if self.socket:
            self.socket.close()
        if self.client:
            self.client.close()
        print "Disconnected"