import sys
import time
import Queue
import threading

from AndroidWifiCon import *
from PCInetCon import *
from ArduinoSerialCon import *

class RPI(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.android = AndroidWifiCon()
        self.pc = PCInetCon()
        self.arduino = ArduinoSerialCon()

        # Create a queue for android, arduino and PC
        self.toPC_q = Queue.Queue(maxsize=0)
        self.toArduino_q = Queue.Queue(maxsize=0)
        self.toAndroid_q = Queue.Queue(maxsize=0)

        # establish connections
        self.arduino.connect()
        self.pc.connectPc()
        self.android.connectAndroid()

        time.sleep(2)

    def read_from_pc(self):
        # pass command from pc to Arduino and Android 
        while True:
            data = self.pc.receivePc()
            if data is not None:
                if (data[:1] == "x" or  data[:1] == "y"):
                    self.toAndroid_q.put_nowait(data)
                    print "pcsendandroid: " + data
		elif (data[:1] == "A"):
		    self.toAndroid_q.put_nowait(data[1:])
                    print "pcsendandroid: " , data[1:]
                else:
                    self.toArduino_q.put_nowait(data)
                    self.toAndroid_q.put_nowait(data)
                    print "pcsendboth: " + data
               

    def read_from_android(self):
        # pass command from android to pc or arduino 
        while True:
            data = self.android.receiveAndroid()
            if data is not None:
                if(data[:1]== "R"):
                    self.toArduino_q.put_nowait(data[1:])
                    print "androidsendarduino: " + data[1:]
                else:
                    self.toPC_q.put_nowait(data)
                    print "androidsendPC: " + data
               

    def read_from_arduino(self):
        # pass command from arduino to pc and android 
        while True:
            data = self.arduino.readArduino()
            if data is not None:
                #self.toAndroid_q.put_nowait("g" + data[:-1] +"z")
		self.toPC_q.put_nowait(data)
                print "arduinosend: " + data


    def write_to_pc(self):
        # write to pc when pc queue is not empty
        while True:	
            if not self.toPC_q.empty():
				data = self.toPC_q.get_nowait()
				self.pc.sendPc(data)
				
    def write_to_android(self):
        # write to android when queue is not empty
        while True:
            if not self.toAndroid_q.empty():
				data = self.toAndroid_q.get_nowait()
				self.android.sendAndroid(data)

    def write_to_arduino(self):
        # write to arduino when queue is not empty
        while True:
            if not self.toArduino_q.empty():
                data = self.toArduino_q.get_nowait()
                self.arduino.writeArduino(data)
                

    def create_threads(self):
        t5 = threading.Thread(target=self.read_from_android)
        t6 = threading.Thread(target=self.write_to_android)
        t1 = threading.Thread(target=self.read_from_pc)
        t2 = threading.Thread(target=self.write_to_pc)
        t3 = threading.Thread(target=self.read_from_arduino)
        t4 = threading.Thread(target=self.write_to_arduino)

        t5.daemon = True
        t6.daemon = True
        t1.daemon = True
        t2.daemon = True
        t3.daemon = True
        t4.daemon = True

        t5.start()
        t6.start()
        t1.start()
        t2.start()
        t3.start()
        t4.start()

        print "All threads initialized and started"

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
