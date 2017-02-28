from AndroidBTCon import *
from ArduinoSerialCon import *
from PCInetCon import *
import threading


def start_communications():
    """
    The communication processes:
    1. Android send the command (beginExplore, run, stop, left, right, forward, reverse)
    2. Rpi do the checking of the command, 
    3. Arduino send to RPI the sensors' value
    4. RPI forwards the sensors' value to PC
    5. PC processes the sensor's value and send the command back to RPI (with map description)
    6a. RPI forwards the command to arduino
    6b. RPi sends the map definition to android (1 way communication)

    TODO:
    The android needs to be able to send command to arduino as well, dunno for what reason.
    Need to ask.


    """
    arduino = ArduinoSerialCon()

    bluetooth = AndroidBTCon()
    bluetooth.connectBluetooth()

    pc = PCInetCon()
    pc.connectPc()

    t1 = threading.Thread(target=arduinoToPC, args=(arduino, pc))
    t1.daemon = True
    t1.start()

    t2 = threading.Thread(target=pcToArduino, args=(arduino, pc))
    t2.daemon = True
    t2.start()

    t3 = threading.Thread(target=rpiToAndroid, args=())
    t3.daemon = True
    t3.start()     


def androidToPC(bluetooth, pc):
    # android send command to pc
    while True:
        command = bluetooth.readBluetooth()
        pc.sendPc(command)


def arduinoToPC(arduino, pc):
    while True:
        data = arduino.readArduino()
        print ("Back to PC "+ data)
        pc.sendPc(data)


def pcToArduinoNAndroid(arduino, pc, bluetooth):
    while True:
        data = pc.receivePc()
        # data here consists of 2 strings separated by comma the first one is the command, 
        # second one is the map description
        print(data)
        if len(data) != 2:
            # checking the data
            continue

        command ,map_des = data.split(",")

        # get the status from the command first =.=
        status = ""
        if command == 'f':
            status = "moving forward"
        elif command == 'l':
            status = "turning left"
        elif command == 'r':
            status = "turning right"

        arduino.writeArduino(command)

        bluetooth.writeBluetooth(status, map_des)




if __name__ == "__main__":
    start_communications()