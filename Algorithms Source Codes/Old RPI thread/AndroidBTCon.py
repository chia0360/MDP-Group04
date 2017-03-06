# -*- coding: utf-8 -*-
"""
Created on Wed Sep 28 22:58:27 2016

@author: lwh92
"""
from bluetooth import *
import subprocess

class AndroidBTCon(object):
    def __init__(self):
        self.server_socket = None
        self.client = None
        self.isConnect = False
        
    def connectBluetooth(self):
        print "goin"
        btPort = 4
        try:
            print "gointry"
            self.server_socket = BluetoothSocket(RFCOMM)
            self.server_socket.bind(("", btPort))
            self.server_socket.listen(1)
            
            self.port = self.server_socket.getsockname()[1]
            uuid = "00001101-0000-1000-8000-00805F9B34FB"
            
            advertise_service( self.server_socket, "MDPGrp004",
                               service_id = uuid,
                               service_classes = [ uuid, SERIAL_PORT_CLASS ],
                               profiles = [ SERIAL_PORT_PROFILE ],)
            subprocess.call(['sudo', 'hciconfig', 'hci0', 'piscan'])
            print "Waiting for BT connection on RFCOMM channel %d" % self.port
            self.client, clientAddress = self.server_socket.accept()
            print "Accepted connection from ", clientAddress
            self.isConnected =True
            return True
        except Exception, e:
            print "Error: %s" %str(e)
            self.server_socket.close()
        except KeyboardInterrupt:
            self.server_socket.close()
            
    def readBluetooth(self):
        print "reading bluetooth"
        try:
            print "reading into command"
            command = ""
            while not command:
                command = self.client.recv(1024)
            print (command)
            return command
        except BluetoothError:
            print "Bluetooth Error. Connection reset by peer. Trying to connect..."
            self.connectBluetooth()
            return "Reconnected"
            
    def writeBluetooth(self,inData):
        try:
            self.client.send(inData)
            print(inData)
        except BluetoothError:
            print "Bluetooth Error. Connection reset by peer. Trying to connect..."
            self.connect_bluetooth()
            return "Reconnected"
            
    def closeBt(self):
        if self.client_socket:
            self.client.close()
            print "Closing client socket"
        if self.server_socket:
                        self.server_socket.close()
                        print "Closing server socket"
        self.bt_is_connected = False


"""
Testing of bluetooth and internet socket tomorrow

bluetooth syncronization steps
will keep try to reconnect to client when the blue tooth disconnected

androidCon = AndroidBTCon()
connected = androidCon.connectBluetooth()
print(connected)
while 1:
    message = androidCon.readBluetooth()
    print (message)
    returnMsg = "Rpi received " + message
    androidCon.writeBluetooth(returnMsg)
"""
