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
        self.algo       = algo.algoFactory(self, algoName='RHR') #Choose which algorithm to use from algo.py
        
        
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
            sensor_data = self.robot.receive()
        robot_direction = self.map.get_robot_direction()
        robot_location  = self.map.get_robot_location()

        verbose('do_read from sensor', sensor_data, tag='Handler', lv='debug')

        dis_x               = [ 0, 1, 0,-1]
        dis_y               = [-1, 0, 1, 0]
        direction_ref       = ['N', 'E', 'S', 'W']
        sensor_loc          = [[-1, 0], [ 0, 1], [ 1, 0], [ 0,-1]]  # sensor's displacement relative to robot location
        sensor_locd         = [[-1,-1], [-1, 1], [ 1, 1], [ 1,-1]]  # diagonal sensor's displacement relative to robot location
        index_displacement  = [0, -4, -1, 3, 1]                 
        index_direction     = [0,  0,  0, 3, 1]                     
        sensor_nbr          = 5

        # front sensor
        index = map.Map.ORIENTATION.index(robot_direction)
        for i in range(sensor_nbr):
            if index_displacement[i] < 0:
                # Sensors: front_right, front_left
                s =  (index - index_displacement[i]) % 4
                loc =  [robot_location[0] + sensor_locd[s][0],
                        robot_location[1] + sensor_locd[s][1]]
            else:
                # Sensors: front_middle, right, left
                s =  (index + index_displacement[i]) % 4
                loc =  [robot_location[0] + sensor_loc[s][0],
                        robot_location[1] + sensor_loc[s][1]]
            verbose('sensor location', loc, tag='Handler', pre='  ')
            
            # Sensor return value
            dis = sensor_data[i]
            if dis < 0:
                dis *= -1
                obs = False
            else:
                obs = True
            # Insert free areas
            y = dis_y[ (index+index_direction [i]) % 4 ]
            x = dis_x[ (index+index_direction [i]) % 4 ]
            for i in range(dis):
                loc[0] += y
                loc[1] += x
                self.map.set_map(loc[0], loc[1], 'free')
            # Insert obstacles
            if (obs):
                self.map.set_map(loc[0], loc[1], 'obstacle')

    # ----------------------------------------------------------------------
    #   Action Commands that robot can receive and carry out
    # ----------------------------------------------------------------------
    def move(self):
        verbose("Action: move forward", tag='Handler')
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
