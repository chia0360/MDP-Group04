import socket
from interface import *

class pc_interface (interface):
   # def __init__(self):
         
    def connect(self):
        try:
	
  	    self.host = "192.168.9.9"
	    self.port = 3000
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#	    self.socket.allow_reuse_address = True
#	    self.socket-setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
	

            self.socket.bind((self.host, self.port))
            self.socket.listen(3)
            print "Waiting for connection from PC."
            
            self.client_sock, self.address = self.socket.accept()
            print "Connected to: ", self.address

           
            #receive the first message from client, know the client address
            #data, self.pcaddr = self.ipsock.recv(1024)
            print("PC Connected")
        except Exception, e:
                print "Error@PCConnect: %s" %str(e)
    
    def disconnect(self):
        try:
            self.socket.close()
        except Exception, e:
            print "Error@PCDisconnect: %s" %str(e)
 
    def writetoPC(self,msg):
        try:
            self.client_sock.sendto(msg, self.address)
            print "Write to PC: %s" %(msg)
        except Exception, e:
            print "Error@PCWrite: %s" %str(e)
            #Added now
            connected = 0
            connected = self.socket.connect()
            while connected == 0:
                self.socket.disconnect
                time.sleep(1)
                self.socket.connect()
 
    def readfromPC(self):
        try:
            #msg, addr = self.ipsock.recvfrom (1024)
            msg = self.client_sock.recv(1024)
            print "Read from PC: %s" %(msg)
            return msg
        except Exception, e:
            print "Error@PCRead: %s" %str(e)
            #Added now
            connected = 0
            connected = self.socket.connect()
            while connected == 0:
                self.socket.disconnect
                time.sleep(1)
                self.socket.connect()
