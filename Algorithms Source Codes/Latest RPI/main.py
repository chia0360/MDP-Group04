import sys
import time
import Queue
import threading

from android_connection import *
from pc_connection import *
from arduino_connection import *

class RPI(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.android = AndroidConnection()
        self.pc = PCConnection()
        self.arduino = ArduinoConnection()

        # Create a queue for android, arduino and PC
        self.toPC = Queue.Queue(maxsize=0)
        self.toArduino = Queue.Queue(maxsize=0)
        self.toAndroid = Queue.Queue(maxsize=0)

        # establish connections
        self.arduino.connect()
        self.pc.connect()
        self.android.connect()

        time.sleep(2)

    def read_from_pc(self):
        # pass command from pc to Arduino or Android 
        while True:
            data = self.pc.readMsg()
            if data is not None:
                if (data[:1] == "x" or  data[:1] == "y"):
                    self.toAndroid.put_nowait(data)
                    print "pc to android: ", data
		elif (data[:1] == "A"):
                    if("f" in data or "l" in data or "r" in data):
                        msg = data[data.find("z")+1]
			self.toArduino.put_nowait(msg)
                        print "pc to arduino: ", msg
		    self.toAndroid.put_nowait(data[1:])
                    print "pc to android: " , data[1:]
                else:
                    self.toArduino.put_nowait(data)
                    self.toAndroid.put_nowait(data)
                    print "pc to both: ", data
               

    def read_from_android(self):
        # pass command from android to pc or arduino 
        while True:
            data = self.android.readMsg()
            if data is not None:
                if(data[:1]== "R"):
                    self.toArduino.put_nowait(data[1:])
                    print "android to arduino: " + data[1:]
                else:
                    self.toPC.put_nowait(data)
                    print "android to pc: " + data
               

    def read_from_arduino(self):
        # pass command from arduino to pc 
        while True:
            data = self.arduino.readMsg()
            if data is not None:
                self.toPC.put_nowait(data)
                print "arduino to pc: " + data

    def write_to_pc(self):
        # write to pc when pc queue is not empty
        while True:
            if not self.toPC.empty():
	        data = self.toPC.get_nowait()
		self.pc.sendMsg(data)
				
    def write_to_android(self):
        # write to android when queue is not empty
        while True:
            if not self.toAndroid.empty():
		data = self.toAndroid.get_nowait()
		self.android.sendMsg(data)

    def write_to_arduino(self):
        # write to arduino when queue is not empty
        while True:
            if not self.toArduino.empty():
                data = self.toArduino.get_nowait()
                self.arduino.sendMsg(data)
                
    def create_threads(self):
        t1 = threading.Thread(target=self.read_from_pc)
        t2 = threading.Thread(target=self.write_to_pc)
        t3 = threading.Thread(target=self.read_from_arduino)
        t4 = threading.Thread(target=self.write_to_arduino)
        t5 = threading.Thread(target=self.read_from_android)
        t6 = threading.Thread(target=self.write_to_android)

        t1.daemon = True
        t2.daemon = True
        t3.daemon = True
        t4.daemon = True
        t5.daemon = True
        t6.daemon = True

        t1.start()
        t2.start()
        t3.start()
        t4.start()
        t5.start()
        t6.start()

        print "All threads started"

    def keep_alive(self):
        while True:
            time.sleep(.5)

if __name__ == "__main__":
    rpi = RPI()
    try:
        rpi.create_threads()
        rpi.keep_alive()
    except KeyboardInterrupt:
        print("Exiting Main")
        rpi.pc.disconnect()
        rpi.android.disconnect()
