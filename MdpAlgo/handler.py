from logger import *
# import simulator
import config
import algo
import map
import robot_simulator
import robot_connector

class Handler:
    def __init__(self, simulator):
        self.simulator  = simulator
        self.map        = map.Map()
        self.algo       = algo.algoFactory(self, algoName='RHR')
        if config.robot_simulation:
            self.robot = robot_simulator.RobotSimulator(self)
            self.__do_read()
        else:
            self.robot = robot_connector.Connector()

    def get_robot_location(self):
        return self.map.get_robot_location()

    def get_robot_direction(self):
        return self.map.get_robot_direction()

    # ----------------------------------------------------------------------
    #   Actions
    # ----------------------------------------------------------------------
    # List of actions that robot can receive
    # ----------------------------------------------------------------------
    def move(self):
        verbose("Action: move forward", tag='Handler')
        self.__do_move()
        self.__do_read()
        self.simulator.update_map()

    def back(self):
        verbose("Action: move backward", tag='Handler')
        cur_dir = self.map.get_robot_direction()
        self.map.set_robot_direction( self.map.get_robot_direction_back() )
        self.__do_move()
        self.map.set_robot_direction( cur_dir )
        self.__do_read()
        self.simulator.update_map()

    def left(self):
        verbose("Action: turn left", tag='Handler')
        self.map.set_robot_direction( self.map.get_robot_direction_left() )
        # self.robot.send('R')
        self.__do_read()
        self.simulator.update_map()
        

    def right(self):
        verbose("Action: turn right", tag='Handler')
        self.map.set_robot_direction( self.map.get_robot_direction_right() )
        self.robot.send('R')
        self.__do_read()
        self.simulator.update_map()


    # ----------------------------------------------------------------------
    #   Real Actions
    # ----------------------------------------------------------------------
    # Sending signal to robot, get the sensors data and process it to map
    # ----------------------------------------------------------------------
    def __do_move(self):
        # Threading
        # map_info.map_lock.acquire()
        # verbose("Locked by "+threading.current_thread(),
        #     tag='Map Lock', lv='debug')
        
        # Getting the next position
        robot_location  = self.map.get_robot_location()
        robot_direction = self.map.get_robot_direction()
        print("__do_move: ", robot_location, robot_direction)
        if   robot_direction == 'N':
                robot_next = [robot_location[0]-1, robot_location[1]]
        elif robot_direction == 'S':
                robot_next = [robot_location[0]+1, robot_location[1]]
        elif robot_direction == 'W':
                robot_next = [robot_location[0], robot_location[1]-1]
        elif robot_direction == 'E':
                robot_next = [robot_location[0], robot_location[1]+1]
        else:
            verbose("ERROR: Direction undefined! __do_move",
                tag='Handler', pre='   >> ', lv='quiet')
        print("next: ", robot_next)
        # Validating the next position
        if self.map.valid_pos(robot_next[0], robot_next[1]):
            # Updating robot position value
            self.map.set_robot_location( robot_next )
            # Send command to robot
            self.robot.send('F')
        else:
            verbose("WARNING: Not moving due to obstacle or out of bound",
                tag='Handler', pre='    ', lv='debug')

        # map_info.map_lock.release()
        # print("[Map Lock] Released by ", threading.current_thread())

    def __do_read(self):
        print("b4 do_read", self.map.get_robot_location())
        sensor_data = None
        while not sensor_data:
            # [front-left, front-right, left, right] 
            sensor_data = self.robot.receive()

        robot_direction = self.map.get_robot_direction()
        robot_location  = self.map.get_robot_location()

        verbose('__do_read from sensor', sensor_data, tag='Handler', lv='debug')

        direction_ref   = ['N', 'E', 'S', 'W']

        # sensor location_offset according to the direction of the robot
        sensor_offset = {'N': [[0, 0], [0, 1], [0, 0], [0, 1]],
                      'E': [[0, 1], [1, 1], [0, 1], [1, 1]],
                      'S': [[1, 1], [1, 0], [1, 1], [1, 0]],
                      'W': [[1, 0], [0, 0], [1, 0], [0, 0]]}

        sensor_nbr      = 4

        idx = map.Map.DIRECTIONS.index(robot_direction)
        for i in range(sensor_nbr):
            if i == 2:
                # left sensor 
                sensor_direction_idx = (direction_ref.index(robot_direction) + 3) % 4
            elif i == 3:
                # right sensor 
                sensor_direction_idx = (direction_ref.index(robot_direction) + 1) % 4
            else:
                # front sensor
                sensor_direction_idx = direction_ref.index(robot_direction)
                
            sensor_direction = direction_ref[sensor_direction_idx]
            # from index and direction we get the position of the sensor
            sensor_loc = sensor_offset[robot_direction][i]
            sensor_loc[0] += robot_location[0]
            sensor_loc[1] += robot_location[1]
            dis = sensor_data[i]
            print("sensor", i, sensor_direction, sensor_loc, dis)
            
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

