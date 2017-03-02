import threading
import time
from map import *
from simulator import *
from handler import *
from robot_connector import *
from descriptor import*

class mul_thread:
    def __init__(self):
        self.simulator  = simulator.Simulator()
        self.handler    = handler.Handler()
        self.descriptor = descriptor.descriptor()
        self.rob_co     = robot_connector.Connector()
        self.rob_co.connect()

    def send_to_rpi(self):
        self.handler.do_read()
        return self.rob_co.send(self.handler.do_read())

    def receive_from_rpi(self):
        action = self.handler.do_read()
    
    def update_map(self):
        s = self.descriptor.descriptor2()
        return s

    def initialise_all_threads(self):
        try:
            thread1 = thread.start_new_thread(send_to_rpi,args = ())
            thread2 = thread.start_new_thread(receive_from_rpi,args = ())
            thread3 = thread.start_new_thread(update_map,args = ())
        except:
            print("Error for some god-damned reason")

x = mul_thread()
x.initialise_all_threads()
thread1.start()
thread2.start()
thread3.start()
#------------------------------
