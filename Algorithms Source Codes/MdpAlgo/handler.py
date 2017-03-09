from logger import *
import config
import algo
import mapclass
import robot_simulator
import robot_connector
import descriptor
import threading
import time

class Handler:
    def __init__(self, simulator):
        self.simulator  = simulator
        self.map        = mapclass.Map()
        self.algo       = algo.algoFactory(self, algoName='RHR') #Choose which algorithm to use from algo.py
        if config.robot_simulation:     #Simulator/Real-World-Test switch
            self.robot = robot_simulator.RobotSimulator(self)
        else:
            self.robot = robot_connector.Connector()
        self.des = descriptor.descriptor()
        self.map_descriptor = None
        self.status = "stop"
        self.recal_counter = 0
        self.delay = 0.5
        self.recalibration = False

    def printMap(self):
        for row in self.map.map:
            print(row)

    def loop(self):
        #command = "fastestPath"
        command = "startexplore" # this will be the command from android
        # uncomment the line below to do integration
        # command = self.robot.receive() 
        print("Receiving :", command)
        
        # 4 corners calibration
        if not self.recalibration:
            position = self.map.get_robot_location()
            right_direction = self.map.get_robot_direction_right()
            print(position)
            if position[0] == 1 and position[1] == 18 and right_direction == 'W':
                self.robot.send('d')
                self.recalibration = True
                self.recal_counter = 0
                time.sleep(self.delay*2)
                return

            if position[0] == 13 and position[1] == 1 and right_direction == 'E':
                self.robot.send('d')
                self.recalibration = True
                self.recal_counter = 0
                time.sleep(self.delay*2)
                return
            
            if position[0] == 13 and position[1] == 18 and right_direction == 'S':
                self.robot.send('d')
                self.recalibration = True
                self.recal_counter = 0
                time.sleep(self.delay*2)
                return
            
        # calibration based on front wall
        if not self.recalibration:
            print("front wall calibration")
            data = None#self.robot.receive()
            self.robot.send('m')
            while not data:
                data = self.robot.receive()

            data = None#self.robot.receive()
            self.robot.send('m')
            while not data:
                data = self.robot.receive()
            # test for front wall
            if (data[1] == 1 and data[2] == 1) or \
                (data[1] == 1 and data[3] == 1) or \
                (data[2] == 1 and data[3] == 1):
                self.robot.send('e')
                self.recalibration = True
                # self.left()
            
            if self.recalibration:
                self.recal_counter = 0
                time.sleep(self.delay*2)
                return

            # # test for right wall
            # if data[4] == 1 and data[5] == 1:
            #     self.robot.send('t')
            #     self.recalibration = True

            # if self.recalibration:
            #     self.recal_counter = 0
            #     time.sleep(self.delay*2)
            #     return   
        

        # repositioning based on walls
        if(self.recal_counter >= 4):
            position = self.map.get_robot_location()
            right_direction = self.map.get_robot_direction_right()
            wall_recalibration = False
            if right_direction == 'N':
                if position[0] == 1:
                    self.right()
                    self.robot.send('e')
                    self.left()
                    wall_recalibration = True
            elif right_direction == 'S':
                if position[0] == self.map.width - 2:
                    self.right()
                    self.robot.send('e')
                    self.left()
                    wall_recalibration = True
            elif right_direction == 'E':
                if position[1] == self.map.length - 2:
                    self.right()
                    self.robot.send('e')
                    self.left()
                    wall_recalibration = True
            elif right_direction == 'W':
                if position[1] == 1:
                    self.right()
                    self.robot.send('e')
                    self.left()
                    wall_recalibration = True

            if wall_recalibration:
                self.recal_counter = 0
                time.sleep(self.delay*2)
                return

        
        print("algo run")
        # first reading before the algo works
        self.do_read()
        self.simulator.update_map()
        # this set of command comes from android
        if command == 'startexplore':
            self.status = "exploring"
            self.algo.explore()
        elif command == 'fastestPath':
            # stop so that the thing will not be affected by the exploration (maybe)
            self.status = "stop"
            shortest_path_moves = self.algo.run()
           # shortest_path_moves = "ffflfrffflfrfflf"

            # will send everything to the arduino in this turn.
            for move in shortest_path_moves:
                self.robot.send(move)
            self.robot.send('\n')
        # the 4 cases below require setting the status of the robot to stop
        # since android is taking over the movement of the robot
        elif command == 'f':
            self.status = "stop"
            self.move()
        elif command == 'l':
            self.status = "stop"
            self.right()
        elif command == 'r':
            self.status = "stop"
            self.left()
        elif command == 'stop':
            self.status = "stop"
        elif ',' in command and self.status == "exploring": 
            self.algo.explore()

        print("sleeping for 2s")
        # delay for some amount of time before doing the reading again to update the map
        # after the robot has moved
        time.sleep(self.delay)
        # self.do_read()
        # self.simulator.update_map()

        # send the map to android, starting with g'xxx'
        # commentted out to test robot movement first
        # self.robot.send("g"+self.algo.des.descriptor2())
        # remind the rpi to change code to take care of this map thingy
        self.recalibration = False
        self.recal_counter += 1

    #Defining Robot's location on map and orientation
    def get_robot_direction(self):
        return self.map.get_robot_direction()
    def get_robot_location(self):
        return self.map.get_robot_location()

    # ----------------------------------------------------------------------
    # Actions of robot
    # ----------------------------------------------------------------------
    def do_move(self):
        robot_direction = self.map.get_robot_direction()
        robot_location  = self.map.get_robot_location()
        # print("moving")
        if   robot_direction == 'N':
                robot_next = [robot_location[0]-1, robot_location[1]]
        elif robot_direction == 'E':
                robot_next = [robot_location[0], robot_location[1]+1]
        elif robot_direction == 'S':
                robot_next = [robot_location[0]+1, robot_location[1]]
        elif robot_direction == 'W':
                robot_next = [robot_location[0], robot_location[1]-1]

        # Next position check and sending command
        print("check for valid position")
        if self.map.valid_pos(robot_next[0], robot_next[1]):
            self.map.set_robot_location( robot_next )
            self.robot.send('f')
            
            
    def do_read(self):

        # in the actual run, the sensor data will be passed from the main loop to do_read
        data = None#self.robot.receive()

        # the loop to wait for sensor is here
        # this will not execute in actual run
        self.robot.send('m')
        while not data:
            print("robot.receive in do_read")
            # this sensor data is in the the following order
            # while not data:
            data = self.robot.receive()
            # left,         front-left, front-middle, front-right, right for real data
            # front_middle, front-left, front-right,  left,        right for simulation
        

        sensor_data = data
        if not config.robot_simulation:
            # swap 0 with 2, then 2 with 3 
            sensor_data[0], sensor_data[2] = sensor_data[2], sensor_data[0]
            sensor_data[3], sensor_data[2] = sensor_data[2], sensor_data[3]
            sensor_data = [int(x) for x in sensor_data]

        robot_direction = self.map.get_robot_direction()
        robot_location  = self.map.get_robot_location()
        print("sensor is")
        print (data)
        print("robot current location", robot_location)
        print("robot current direction", robot_direction)

        direction_ref   = ['N', 'E', 'S', 'W']

        # sensor location_offset according to the direction of the robot
        # front_middle, front-left, front-right,  left,        right
        sensor_offset = {'N': [[-1, 0], [-1, -1], [-1, 1], [-1, -1], [-1, 1]],
                         'E': [[0, 1], [-1, 1], [1, 1], [-1, 1], [1, 1]],
                         'S': [[1, 0], [1, 1], [1, -1], [1, 1], [1, -1]],
                         'W': [[0, -1], [1, -1], [-1, -1], [1, -1], [-1, -1]]}

        sensor_nbr      = 5

        for i in range(sensor_nbr):
            if i == 3:
                # left sensor 
                sensor_direction_idx = (direction_ref.index(robot_direction) + 3) % 4
            elif i == 4:
                # right sensor 
                sensor_direction_idx = (direction_ref.index(robot_direction) + 1) % 4
            else:
                # front sensors
                sensor_direction_idx = direction_ref.index(robot_direction)
                
            sensor_direction = direction_ref[sensor_direction_idx]
            # from index and direction we get the position of the sensor
            sensor_loc = sensor_offset[robot_direction][i]
            sensor_loc[0] += robot_location[0]
            sensor_loc[1] += robot_location[1]

            dis = sensor_data[i]
            # print("sensor", i, sensor_direction, sensor_loc, dis)
            
            # negative dis means not obstructed
            if dis < 0:
                dis *= -1
                obs = False
            else:
                obs = True
            # set the free boxes

            if sensor_direction == 'N':
                dx = 0
                dy = -1
            elif sensor_direction == 'S':
                dx = 0
                dy = 1
            elif sensor_direction == 'E':
                dx = 1
                dy = 0
            elif sensor_direction == 'W':
                dx = -1
                dy = 0
            else:
                dx = 0
                dy = 0
            
            # open the map one by one from the location of the sensor
            loc = sensor_loc[:]
            
            for i in range(dis):
                loc[0] += dy
                loc[1] += dx
                self.map.set_map(loc[0], loc[1], 'free')
            # set if obstacle
            if obs:
                self.map.set_map(loc[0], loc[1], 'obstacle')
        return sensor_data

        print("end do_read")

    
    def move(self):
        # sending the command in do_move()
        self.do_move()

    def back(self):
        cur_dir = self.map.get_robot_direction()
        self.map.set_robot_direction( self.map.get_robot_direction_back() )
        self.do_move()
        self.map.set_robot_direction( cur_dir )

    def left(self):
        self.map.set_robot_direction( self.map.get_robot_direction_left() )
        self.robot.send('l')

    def right(self):
        self.map.set_robot_direction( self.map.get_robot_direction_right() )
        self.robot.send('r')


    # ---------------------------------End of Class-------------------------------------
