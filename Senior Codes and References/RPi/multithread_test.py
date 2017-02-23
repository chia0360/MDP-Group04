import thread
import time
import Queue
import os
import sys

from interface import *
from pc_interface import *
from android_interface import *
from arduino_interface import *

#algo 
from Map import *
from Robot import *

class Main:
        ExploreOrFast = 1
	def __init__(self):
		#check if running from root
		if not os.geteuid()==0:
			sys.exit("Error: You must be root to run this application")

		#Initialize the fucking bluetooth
		os.system("sudo hciconfig hci0 piscan")

                #Initialize Queues
                self.toAndroid = Queue.Queue(maxsize=0)
                self.toRobot = Queue.Queue(maxsize=0)
                self.toPC = Queue.Queue(maxsize=0)
                self.toAlgo = Queue.Queue(maxsize=0)
                
                #Create interface objects
                self.bt = android_interface()
                self.pc = pc_interface()
                self.robot = arduino_interface()


        def connectBT(self):
                #connect bluetooth
                connected = 0
                while connected == 0:
                        #self.bt.disconnect()
                        #time.sleep(1)
                        connected = self.bt.connect()

        def connectPC(self):
                #connect PC
                connected = 0
                connected = self.pc.connect()
                while connected == 0:
                        self.pc.disconnect()
                        time.sleep(1)
                        connected = self.pc.connect()

        def connectArduino(self):    
                #connect arduino
                connected = 0
                connected = self.robot.connect()
                while connected == 0:
                        time.sleep(1)
                        connected = self.robot.connect()


        #I/O for algo
        def activateAlgo(self, algoQ, robotQ, androidQ, pcQ):
                robot = Robot(1,1,1,'U')
	#	robot = Robot(1,1,1,'R')
                map=Map(15,20)

		global ExploreOrFast	
		ExploreOrFast = 1

		#TEST
#		ExploreOrFast = 0
#		val = "RMMMLMMMMMMMMMMMMMRMMLMRMMMMMMLMMMRM"
#		robot.pathCommand = val
#		robot.X = 1
#		robot.Y = 1
#		robot.Dir = "U"
#		robot.fastestPathDecoder()
 #               algoQ.put_nowait("999")
#		time.sleep(3)
#		robotQ.put_nowait("h")
#		time.sleep(2)
#		algoQ.get_nowait()
#		self.robot.flush()
		#END TEST
                
                while 1:
                        if not algoQ.empty():
				val = algoQ.get_nowait()

				if ExploreOrFast == 0:
					#call algo fastest path
					out = robot.fastestRun(val)

					if out == "F":
						print "Fastest path complete, final realignment"
						#proto
					#	algoQ.put_nowait("999")
					#	while 1:
					#		if not algoQ.empty():
					#			val = algoQ.get_nowait()
					#			out = robot.goalzoneRealign()
					#			if out == "C":
					#				break
					#			robotQ.put_nowait(out)
					#			time.sleep(1)
					
						#end proto
						print "Complete, lohyehmohyeh"
						break

					robotQ.put_nowait(out)

					pcQ.put_nowait(robot.mapStr)
					androidQ.put_nowait(robot.androidMapStr)
					
					#delay
					if out == 3 or out == 2:
						print "delaying 0.3s for post-turn or post 3 grid"
						time.sleep(0.3)
				
						
				
				elif ExploreOrFast == 1:
					out = robot.explore(val)
					if out[0] != "F":
				
                                		robotQ.put_nowait(out)
						#get long string and pass to pc
						pcQ.put_nowait(robot.mapStr)
						androidQ.put_nowait(robot.androidMapStr)
					else:
				
						print "Exploration ended, realigning now..."

						while robot.Dir[0] != "U":
							robotQ.put_nowait(robot.startZoneRealign())
							time.sleep(3)
						

						androidQ.put_nowait(robot.androidMapStr)


						robot.fastestPathCompute()

						#print "Waiting 10 seconds..."
						#time.sleep(10)

						algoQ.put_nowait("A")
			
						while not algoQ.empty():
							val = algoQ.get_nowait()
							if val[0] == "A":
								#print "Received fastest path from PC, sending to decoder..."
								#robot.fastestPathDecoder(val)

								#wait here
								t0 = time.time()
								print "READY for tablet command to begin..."									
								while 1:
									if not algoQ.empty():
										val = algoQ.get_nowait()

										if val[0] == "f":
											break
									else:
										print time.time()- t0, "seconds elapsed of 30s"
										if time.time() - t0 >= 30:
											robotQ.put_nowait("f")
											break


								algoQ.put_nowait("999")
								print "Beginning fastest run..."
								ExploreOrFast = 0
								break
					
					
                            
                      
                
        #sending data to android from queue
        def btWrite(self, androidQ):
                while 1:
                        if not androidQ.empty():
                                val = androidQ.get_nowait()
                                self.bt.writetoBT(val)                             

        #reading android value, send data to arduino (and/or pc).
        def btRead(self, robotQ, pcQ, algoQ):
                global ExploreOrFast
		while 1:
                        val = self.bt.readfromBT()
			if ExploreOrFast == 0:
				print "Closing btRead..."
				break
                        if val is not None:
				robotQ.put_nowait(val)
				if val[0] == "f":
					algoQ.put_nowait(val)
			
                                #robotQ.put_nowait(val)
                                #algoQ.put_nowait(val) #testing
                                #pcQ.put_nowait(val)
		return

        #sending data to PC from PC msg queue.
        def pcWrite(self, pcQ):
                while 1:
                        if not pcQ.empty():
                                val = pcQ.get_nowait()
                                self.pc.writetoPC(val)

        #reading data from PC, send data to algoQ
        def pcRead(self, algoQ):
	   global ExploreOrFast
           while 1:
                   val = self.pc.readfromPC()
                   if ExploreOrFast == 0:
			   print "Closing pcRead..."
			   break
                   if val is not None:
                           algoQ.put_nowait(val)

	   return

        #sending data to arduino from arduino msg queue.
        def robotWrite(self, robotQ):
           self.robot.flush()
#	   time.sleep(3)
#	   robotQ.put_nowait("h")
#	   self.robot.flush()
           while 1:
                  if not robotQ.empty():
                         val = robotQ.get_nowait()
                         self.robot.writetoSR(val + "\n")
                 
        #reading data from arduino to ALGO & android.
        def robotRead(self, pcQ, androidQ, algoQ):
           while 1:
                   val = self.robot.readfromSR()
                   if val is not None:
                        if val[0] != 'D':
                           #androidQ.put_nowait(val)
                           algoQ.put_nowait(val)
                           #pcQ.put(val)
                 
        #starting all thread.
        def startThread(self):
                try:
                        thread.start_new_thread( self.btWrite, (self.toAndroid,))
                        thread.start_new_thread( self.btRead, (self.toRobot, self.toPC, self.toAlgo))
                        thread.start_new_thread( self.pcWrite, (self.toPC,))
                        #thread.start_new_thread( self.pcRead, (self.toAlgo,))
                        thread.start_new_thread( self.robotWrite, (self.toRobot,))
                        thread.start_new_thread( self.robotRead, (self.toPC, self.toAndroid, self.toAlgo))
                        thread.start_new_thread( self.activateAlgo, (self.toAlgo, self.toRobot, self.toAndroid, self.toPC))

                except Exception, e:
                        print "Unable to start thread!"
                        print "Error: %s" %str(e) 
                while 1:
                   pass
           
test = Main()
test.connectArduino()
test.connectPC()
test.connectBT()
test.startThread()
