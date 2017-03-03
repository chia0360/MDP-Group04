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

    def printMap(self):
        for row in self.map.map:
            print(row)

    def loop(self):
        start_time = time.time()
    # while True:
        # get command
        # command = self.robot.receive()
        # for testing
        command = "explore" # this will be the command from android
        # sensor = self.robot.receive() # this will be the sensors
        print("Receiving :", command)
        # check command

        
        # this set of command comes from android
        if command == 'explore':
            self.do_read()
            self.algo.explore()
            self.status = "exploring"
            time.sleep(2)
            self.do_read()
            self.simulator.update_map()
        # elif command == 'run':
        #     self.algo.run()
        # elif command == 'f':
        #     self.move()
        # elif command == 'tr':
        #     self.right()
        # elif command == 'tl':
        #     self.left()
        elif command == 'stop':
            self.status = "stop"
        # elif ',' in command and self.status == "exploring": 
        #     # if its not a command from android, its probably the sensors' data
        #     self.do_read(command) 
        #     # read the sensors when the robot stop.
        #     self.simulator.update_map()
        #     print("before explore")
        #     self.algo.explore(True)
        #     # from the sensors' values determine the step to move
        #     # the algo will send command to robot in this step
        #     print("sleep 1")
        #     time.sleep(1)
        #     # we need to wait for the robot to execute the command
        #     # then update the simulator
        #     self.simulator.update_map()
        #     # this will update robot position


        # for empty command from android, we just continue exploring
        elif self.status == "exploring":
            self.do_read()
            self.algo.explore()
            time.sleep(2)
            self.do_read()
            self.simulator.update_map()
        print("handler loop takes", time.time() - start_time)

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
        data = self.robot.receive()

        # the loop to wait for sensor is here
        # this will not execute in actual run
        while not data:
            print("robot.receive in do_read")
            # this sensor data is in the the following order
            data = self.robot.receive()
            # left,         front-left, front-middle, front-right, right for real data
            # front_middle, front-left, front-right,  left,        right for simulation
        
        print("sensor is")
        print (data)
        sensor_data = data
        if not config.robot_simulation:
            # swap 0 with 2, then 2 with 3 
            sensor_data[0], sensor_data[2] = sensor_data[2], sensor_data[0]
            sensor_data[3], sensor_data[2] = sensor_data[2], sensor_data[3]
            sensor_data = [int(x) for x in sensor_data]

        robot_direction = self.map.get_robot_direction()
        robot_location  = self.map.get_robot_location()

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

    # ----------------------------------------------------------------------
    #   Action Commands that robot can receive and carry out
    # ----------------------------------------------------------------------
    def move(self):
        # sending the command in do_move()
        self.do_move()
        # not necessary to update map here in actual run
        # because the loop will get the next value of the sensor 
        # self.do_read()
        # self.simulator.update_map()

    def back(self):
        cur_dir = self.map.get_robot_direction()
        self.map.set_robot_direction( self.map.get_robot_direction_back() )
        self.do_move()
        self.map.set_robot_direction( cur_dir )
        # self.do_read()
        # self.simulator.update_map()

    def left(self):
        self.map.set_robot_direction( self.map.get_robot_direction_left() )
        # Send command to robot
        self.robot.send('l')
        # self.do_read()
        # self.simulator.update_map()

    def right(self):
        self.map.set_robot_direction( self.map.get_robot_direction_right() )
        # Send command to robot
        self.robot.send('r')
        # self.do_read()
        # self.simulator.update_map()
   


    # ---------------------------------End of Class-------------------------------------