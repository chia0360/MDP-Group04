import socket
import time

class AndroidWifiCon():

	def __init__ (self):
		self.connection = None
		self.s = None

	def write_android(self,msg):
		print ("Write to Android: ", msg)
		msg += '\n'
		self.connection.send(msg.encode())

	def read_android(self):
		msg = self.connection.recv(1024).decode(encoding="UTF-8")
		print "Received from Android: ", msg
		return msg

	def start_rpi(self):
		self.s = socket.socket()
		host = '192.168.4.1'
		portnumber = 8765
		self.s.bind((host, portnumber))
		self.s.listen(5)

		print "Awaiting Client Connection..."
		self.connection, addr = self.s.accept()

		print "Client from", addr, host, "at port number", portnumber, "connected", time.ctime()
		print "Android to Rpi connection started"

	def stop_rpi(self):
		self.s.stop()


if __name__ == "__main__":

	try:
		pibot = AndroidWifiCon()
		pibot.start_rpi()
		pibot.write_android("HALO")
		while True:
			pibot.read_android()
	except KeyboardInterrupt:
		pibot.stop_rpi()

