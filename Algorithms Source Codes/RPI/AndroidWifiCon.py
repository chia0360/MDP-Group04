import socket
import time

class AndroidWifiCon():

        def __init__ (self):
                self.connection = None
                self.s = None

        def write_Rpi(self,msg):
                print ("Write to RPi ", msg)
                msg += '\n'
                self.connection.send(msg.encode())

        def read_Rpi(self):
                msg = self.connection.recv(1024).decode(encoding="UTF-8")
                print "Received from Rpi", msg
                return msg

        def start_Rpi(self):
                self.s = socket.socket()
                host = '192.168.4.1'
                portnumber = 8765
                self.s.bind((host, portnumber))
                self.s.listen(5)

                print "Awaiting Client Connection..."
                self.connection, addr = self.s.accept()

                print "Client from", addr, host, "at port number", portnumber, "connected", time.ctime()
                print "Android to Rpi connection started"

        def stop_pc(self):
                self.s.stop()


if __name__ == "__main__":

        try:
                pibot = AndroidWifiCon()
                pibot.start_Rpi()
                while True:
                        pibot.read_Rpi()
        except KeyboardInterrupt:
                pibot.stop_R()

