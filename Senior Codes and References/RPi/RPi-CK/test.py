import thread
import time
import Queue
import os
import sys

#from interface import *
from arduino_interface import *

class Main:
        def __init__(self):

                #Create interface objects
                self.robot = arduino_interface()

        def connectArduino(self):    
                #connect arduino
                connected = 0
                connected = self.robot.connect()
                while connected == 0:
                        time.sleep(1)
                        connected = self.robot.connect()
                        

        #sending data to arduino from arduino msg queue.
        def robotWrite(self):
           self.robot.flush()
           while 1:
                   x = (raw_input())
                   self.robot.writetoSR(x + "\n")
                 
        #reading data from arduino
        def robotRead(self):
           while 1:
                   val = self.robot.readfromSR()
                   if val is not None:
                           time.sleep(0)
                 
        #starting all thread.
        def startThread(self):
                try:
                        thread.start_new_thread( self.robotWrite,())
                        thread.start_new_thread( self.robotRead,())
                except Exception, e:
                        print "Unable to start thread!"
                        print "Error: %s" %str(e) 
                while 1:
                   pass
           
test = Main()
test.connectArduino()
test.startThread()
