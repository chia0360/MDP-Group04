import socket
import string
import time
import threading


# Dummy client code

class Test(threading.Thread):
        def __init__(self):
                threading.Thread.__init__(self)
                self.ip = "192.168.10.10" # Connecting to IP address of MDPGrp2
                self.port = 5182


                # Create a TCP/IP socket
                self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.client_socket.connect((self.ip, self.port))

        # Send data
        def write(self, count = 0):
                print "\nEnter text to send: "
                msg = raw_input()
                while True:
                        # time.sleep(1)
                        self.client_socket.send(msg)
                        print "\nEnter text to send: "
                        msg = raw_input()
                       # msg ="HA90|"
                        count += 1
                print "quit write()"


        # Receive data
        def receive(self):
                while True:
                        data = self.client_socket.recv(1024)
                        if len(data) == 0:
                                print "quitting..."
                                break
                        print "\nFrom rpi: %s " % data
                print "quit receive()"
        
        def keep_main(self):
                while True:
                        time.sleep(0.5)



if __name__ == "__main__":
        test = Test()

        rt = threading.Thread(target = test.receive)
        wt = threading.Thread(target = test.write)

        rt.daemon = True
        wt.daemon = True

        wt.start()
        rt.start()
        
        print "start rt and wt"

        test.keep_main()

        # Close connections
        self.client_socket.close()
        print "End of client program"
