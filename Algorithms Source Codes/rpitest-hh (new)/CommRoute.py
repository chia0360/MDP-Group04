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

        # Create a queue for each connection
        self.toPC_q = Queue.Queue(maxsize=0)
        self.toArduino_q = Queue.Queue(maxsize=0)
        self.toAndroid_q = Queue.Queue(maxsize=0)

        # Establish connections
        self.pc.connectPc()
        self.arduino.connect()
        self.android.connectAndroid()

        time.sleep(2)

    def read_from_pc(self):
        # what is read from pc will be added to toArduino_q and toAndroid_q
        while True:
            data = self.pc.receivePc()
            if data is not None:
                self.toArduino_q.put_nowait(data)
                self.toAndroid_q.put_nowait(data)
                # wait a while between reads
                time.sleep(2)

    def read_from_android(self):
        # what is read from android will be added to toPC_q
        while True:
            data = self.android.receiveAndroid()
            if data is not None:
                self.toPC_q.put_nowait(data)
                # wait a while between reads
                time.sleep(2)

    def read_from_arduino(self):
        # what is read from arduino will be added to toPC_q 
        while True:
            data = self.arduino.readArduino()
            if data is not None:
                self.toPC_q.put_nowait(data)
                # wait a while between reads
                time.sleep(2)


    def write_to_pc(self):
        while True:	
            if not self.toPC_q.empty():
				data = self.toPC_q.get_nowait()
				self.pc.sendPc(data)
                # wait a while between writes
				time.sleep(2)


    def write_to_android(self):
        while True:
            if not self.toAndroid_q.empty():
				print("writing to android")
				data = self.toAndroid_q.get_nowait()
				self.android.sendAndroid(data+'\n')
                # wait a while between writes
				time.sleep(2)

    def write_to_arduino(self):
        while True:
            if not self.toArduino_q.empty():
                data = self.toArduino_q.get_nowait()
                self.arduino.writeArduino(data)
                # wait a while between writes
                time.sleep(2)


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
