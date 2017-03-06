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
            print "Waiting for incomming connection"
            self.client, self.address = self.socket.accept()
            print "Connected to: ", self.address
            return True
        except Exception, e:
            print "Fail to open socket connection", str(e)
            self.socket.close()
            if self.client is not None:
                self.client.close()

    def sendAndroid(self,outData):
        time.sleep(.05)
        print("write to android", outData)
        outData += '\n'
        try:
            self.client.send(outData.encode())
        except Exception, e:
            print "Fail to send data", str(e)
            self.connectAndroid()

    def receiveAndroid(self):
        time.sleep(.05)
        try:
            message = self.client.recv(1024)
            print("receiveAndroid", message)
            return message
        except Exception, e:
            print "Fail to receive data", str(e)
            self.connectAndroid()

   def disconnect(self):
        if self.socket:
            self.socket.close()
        if self.client:
            self.client.close()
        print "Disconnected"


PC = AndroidWifiCon()
data = "1"
if(PC.connectAndroid()):
        #PC.write_to_socket("Hello, talk to me")
    while(data != '-1'):
        print (data)
        data = PC.receiveAndroid()
        print (data)
        if (data != '-1' or data == None):
            print data
            data = "I received: " + data
            PC.sendAndroid(data)


