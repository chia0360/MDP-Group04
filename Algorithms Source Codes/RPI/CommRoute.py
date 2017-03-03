import sys
import time
import Queue
# from AndroidBTCon import *
from ArduinoSerialCon import *
from PCInetCon import *
import threading
import serial


class RPI(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.pc = PCInetCon()
        self.arduino = ArduinoSerialCon()

        # Create a queue for each connection
        # maxsize=0 => infinite size queue
        # self.toPC_q = Queue.Queue(maxsize=0)
        # self.toArduino_q = Queue.Queue(maxsize=0)

        # try to acquire connections
        self.pc.connectPc()
        self.arduino.connect()

        # before the thread to actually start
        # since we are calling create_threads() right after this in main()
        time.sleep(2)


    def pc_to_arduino(self):
        while True:
            data = self.pc.receivePc()
            print("data from pc", data)
            if data is not None and data != "":
                self.arduino.writeArduino(data)
            # time.sleep(.1)

    def arduino_to_pc(self):
        while True:
            print("arduino_to_pc")
            data = self.arduino.readArduino()
            if data is not None and data != "":
                self.pc.sendPc(data)
            # all_data = data.split(" ")
            # print("after splitting", all_data)
            # print("taking in the second last data")
            # new_data = all_data[-1]
            # if len(all_data) > 1:
            #     new_data = all_data[-2]
            # # sensor values
            # time.sleep(.1)    

    # def read_from_pc(self):
    #     # what is read from pc will be passed to toArduino_q 
    #     while True:
    #         data = self.pc.receivePc()
    #         if data is not None:
    #             self.toArduino_q.put_nowait(data)
    #             # wait a while between reads
    #             time.sleep(2)


    # def read_from_arduino(self):
    #     # what is read from arduino will be passed to toPC_q 
    #     while True:
    #         data = self.arduino.readArduino()
    #         if data is not None:
    #             # clear the queue
    #             with self.toPC_q.mutex:
    #                 self.toPC_q.queue.clear()                
    #             self.toPC_q.put_nowait(data)
    #             # wait a while between reads
    #             time.sleep(2)


    # def write_to_pc(self):
    #     # consume the data from the queue
    #     while True:
    #         if not self.toPC_q.empty():
    #             data = self.toPC_q.get_nowait()
    #             self.pc.sendPc(data)
    #             # wait a while between writes
    #             time.sleep(2)


    # def write_to_arduino(self):
    #     # consume the data from the queue
    #     while True:
    #         if not self.toArduino_q.empty():
    #             data = self.toArduino_q.get_nowait()
    #             self.arduino.writeArduino(data)
    #             # wait a while between writes
    #             time.sleep(2)


    def create_threads(self):
        t1 = threading.Thread(target=self.pc_to_arduino)
        t2 = threading.Thread(target=self.arduino_to_pc)

        t1.daemon = True
        t2.daemon = True
        
        t1.start()
        t2.start()

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