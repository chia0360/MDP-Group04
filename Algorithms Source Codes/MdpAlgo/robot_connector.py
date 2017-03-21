import socket
from robot import *
import re
import time


class Connector(Robot):
    def __init__(self):

        family = socket.AF_INET
        socket_type = socket.SOCK_STREAM
        self.socket = socket.socket(family, socket_type)
        self.socket.settimeout(1)
        self.connected = False
        self.connect()
        self.m_counter = 0

    def connect(self):
        host = '192.168.4.1'
        port = 8888
        try:
            self.socket.connect((host, port))
        except Exception:
            print("[Error] Unable to establish connection.")
        else:
            self.connected = True
            print("[Info] Connection established.")

    def send(self, msg):
        if not self.connected:
            self.connect()
        if self.connected:
            if (msg == 'm'):
                self.m_counter+=1
            print("[Info] Sending message: ", msg)
            try:
                self.socket.sendall(str.encode(msg))
            except Exception:
                print("[Error] Unable to send message. Connection loss.")
                # self.connected = False

    def receive(self):
        # robot connector will only interface with rpi, receiving sensor's value
        # android will be connected to pc to send command through another interface
        if not self.connected:
            self.connect()
        if self.connected:
            try:
                msg = self.socket.recv(1024)
                if msg:
                    # this message will contain all set of sensors' value upto the time of
                    # issueing the socket receive
                    print ("message: ", msg)
                    msg = msg.decode()
                    msg_decoded = re.sub(r'[^\x00-\x7f]',r'', msg)
                    if "," not in msg_decoded:
                        # this is a command from android
                        return msg_decoded
                    else:    
                        # # msg_decoded = "-2,-2,-2,-2,-2"
                        # print("[Info] Received: ", msg_decoded)
                        # # we thus need to separate each set of sensors' values
                        messages = msg_decoded.split("\n")
                        print("messages:", messages)
                        mess = messages.pop()
                        # this loop will help removing the empty readings
                        while len(mess) == 0:
                            mess = messages.pop()
                        # for a incomplete set of sensors

                        # we now receive only one set of values from sensor
                        splited_mess = mess.split(",")
                        while len(splited_mess) != 7 or len(splited_mess[1]) == 0 or len(splited_mess[5]) == 0:
                            mess = messages.pop()
                            splited_mess = mess.split(",")
                            # this is malformed sensors' values 
                            # splited_mess = mess.split(",")
                            # we will keep popping the previous set of sensor value if the 
                            # current one is not a 5-value comma separated message
                            # this will also check if the first value and the last value is empty
                        # now we return the integer set of sensors' value
                        self.send('Ag' + ','.join(splited_mess) + 'z')
                        print ("robot connector returning: ", splited_mess)
                        print ("header: ", splited_mess[0])
                        print ("[Info] M counter is", self.m_counter)
                        print("the funny character from arduino", splited_mess[6])
                        time.sleep(.3)
                        splited_mess = [int(x) for x in splited_mess[:6]][1:]
                        # if self.m_counter != splited_mess[0]:
                        #     return None
                        return splited_mess
            except socket.timeout:
                print("[Info] No message received.")
        # else:
        #     print("[Error] Unable to receive message. Connection loss.")

# if __name__ == "__main__":
# 	crobot = Connector()
# 	crobot.connect()
# 	while True:
# 		crobot.send("fine")
