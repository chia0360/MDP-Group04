from logger import *
import config
import algo
import map
import robot_simulator
import robot_connector

class Handler:
    def __init__(self, simulator):
        self.simulator  = simulator
        self.map        = map.Map()
        self.algo       = algo.algoFactory(self, algoName='BF1') #Choose which algorithm to use from algo.py
        
        
        if config.robot_simulation:     #Simulator/Real-World-Test switch
            self.robot = robot_simulator.RobotSimulator(self)
            self.do_read()
        else:
            self.robot = robot_connector.Connector()

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
        
        if   robot_direction == 'N':
                robot_next = [robot_location[0]-1, robot_location[1]]
        elif robot_direction == 'E':
                robot_next = [robot_location[0], robot_location[1]+1]
        elif robot_direction == 'S':
                robot_next = [robot_location[0]+1, robot_location[1]]
        elif robot_direction == 'W':
                robot_next = [robot_location[0], robot_location[1]-1]
        else:
            verbose("ERROR: Direction entry is invalid! do_move",
                tag='Handler', pre='   >> ', lv='quiet')

        # Next position check and sending command
        if self.map.valid_pos(robot_next[0], robot_next[1]):
            self.map.set_robot_location( robot_next )
            self.robot.send('F')
        else:
            verbose("WARNING: Can't move (obstacle/out-of-bounds)",
                tag='Handler', pre='    ', lv='debug')

    def do_read(self):
        sensor_data = None
        while not sensor_data:
            # this sensor data is in the the following order
            sensor_data = self.robot.receive()
            # left,         front-left, front-middle, front-right, right for real data
            # front_middle, front-left, front-right,  left,        right for simulation

            if not config.robot_simulation:
                sensor_data = map(int, list(sensor_data))
                # swap 0 with 2, then 2 with 3 
                sensor_data[0], sensor_data[2] = sensor_data[2], sensor_data[0]
                sensor_data[3], sensor_data[2] = sensor_data[2], sensor_data[3]
                 
        robot_direction = self.map.get_robot_direction()
        robot_location  = self.map.get_robot_location()

        verbose('do_read from sensor', sensor_data, tag='Handler', lv='debug')

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
        verbose("Action: move forward", tag='Handler')
        self.robot.send('F')
        self.do_move()
        self.do_read()
        self.simulator.update_map()

    def back(self):
        verbose("Action: move backward", tag='Handler')
        cur_dir = self.map.get_robot_direction()
        self.map.set_robot_direction( self.map.get_robot_direction_back() )
        self.do_move()
        self.map.set_robot_direction( cur_dir )
        self.do_read()
        self.simulator.update_map()

    def left(self):
        verbose("Action: turn left", tag='Handler')
        self.map.set_robot_direction( self.map.get_robot_direction_left() )
        # Send command to robot
        self.robot.send('L')
        self.do_read()
        self.simulator.update_map()

    def right(self):
        verbose("Action: turn right", tag='Handler')
        self.map.set_robot_direction( self.map.get_robot_direction_right() )
        # Send command to robot
        self.robot.send('R')
        self.do_read()
        self.simulator.update_map()
   


    # ---------------------------------End of Class-------------------------------------
