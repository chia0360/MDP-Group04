import threading
import socket
class PCInet1Con(object):
    def __init__(self):
        self.port = 8765
        self.host = "192.168.4.1"
        self.socket = None
        self.client = None
        self.address = None

    def connectPc(self):
        print "using connectPC"
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.socket.bind((self.host, self.port))
            self.socket.listen(5)
            print "Waiting for incomming connection"
            self.client, self.address = self.socket.accept()
            print "Connected to: ", self.address
            return True
        except Exception, e:
            print "Fail to open socket connection", str(e)
            self.socket.close()

    def sendPc(self,outData):
        try:
            self.client.send(outData)
        except Exception, e:
            print "Fail to send data", str(e)

    def receivePc(self):
        try:
            return self.client.recv(1024)
        except Exception, e:
            print "Fail to receive data", str(e)


    def disconnect(self):
        if self.socket:
            self.socket.close()
        if self.client:
            self.client.close()
        print "Disconnected"


