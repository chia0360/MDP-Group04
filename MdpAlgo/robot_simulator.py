from logger import *
from robot import *


class RobotSimulator(Robot):
    def __init__(self, handler):
        self.map_info       = handler.map


    def get_front_left(self):
        detect_range = config.sensor_range['front_left']
        robot_location = self.map_info.get_robot_location()
        direction = self.map_info.get_robot_direction()
        if direction == 'E':
            sensor_location = [robot_location[0], robot_location[1]+1]
            return self.get_sensor_data(sensor_location, 'E', detect_range)
        elif direction == 'W':
            sensor_location = [robot_location[0]+1, robot_location[1]]
            return self.get_sensor_data(sensor_location, 'W', detect_range)
        elif direction == 'S':
            sensor_location = [robot_location[0]+1, robot_location[1]+1]
            return self.get_sensor_data(sensor_location, 'S', detect_range)
        elif direction == 'N':
            sensor_location = [robot_location[0], robot_location[1]]
            return self.get_sensor_data(sensor_location, 'N', detect_range)
        else:
            print("    [ERROR] Invalid direction!")
            return

    def get_front_right(self):
        detect_range = config.sensor_range['front_right']
        robot_location = self.map_info.get_robot_location()
        direction = self.map_info.get_robot_direction()
        if direction == 'E':
            sensor_location = [robot_location[0]+1, robot_location[1]+1]
            return self.get_sensor_data(sensor_location, 'E', detect_range)
        elif direction == 'W':
            sensor_location = [robot_location[0], robot_location[1]]
            return self.get_sensor_data(sensor_location, 'W', detect_range)
        elif direction == 'S':
            sensor_location = [robot_location[0]+1, robot_location[1]]
            return self.get_sensor_data(sensor_location, 'S', detect_range)
        elif direction == 'N':
            sensor_location = [robot_location[0], robot_location[1]+1]
            return self.get_sensor_data(sensor_location, 'N', detect_range)
        else:
            print("    [ERROR] Invalid direction!")
            return

    def get_left(self):
        detect_range = config.sensor_range['left']
        robot_location = self.map_info.get_robot_location()
        direction = self.map_info.get_robot_direction()
        if direction == 'E':
            sensor_location = [robot_location[0], robot_location[1]+1]
            return self.get_sensor_data(sensor_location, 'N', detect_range)
        elif direction == 'W':
            sensor_location = [robot_location[0]+1, robot_location[1]]
            return self.get_sensor_data(sensor_location, 'S', detect_range)
        elif direction == 'S':
            sensor_location = [robot_location[0]+1, robot_location[1]+1]
            return self.get_sensor_data(sensor_location, 'E', detect_range)
        elif direction == 'N':
            sensor_location = [robot_location[0], robot_location[1]]
            return self.get_sensor_data(sensor_location, 'W', detect_range)
        else:
            print("    [ERROR] Invalid direction!")
            return

    def get_right(self):
        detect_range = config.sensor_range['right']
        robot_location = self.map_info.get_robot_location()
        direction = self.map_info.get_robot_direction()
        if direction == 'E':
            sensor_location = [robot_location[0]+1, robot_location[1]+1]
            return self.get_sensor_data(sensor_location, 'S', detect_range)
        elif direction == 'W':
            sensor_location = [robot_location[0], robot_location[1]]
            return self.get_sensor_data(sensor_location, 'N', detect_range)
        elif direction == 'S':
            sensor_location = [robot_location[0]+1, robot_location[1]]
            return self.get_sensor_data(sensor_location, 'W', detect_range)
        elif direction == 'N':
            sensor_location = [robot_location[0], robot_location[1]+1]
            return self.get_sensor_data(sensor_location, 'E', detect_range)
        else:
            print("    [ERROR] Invalid direction!")
            return

    # ----------------------------------------------------------------------
    #   Function get_sensor_data
    # ----------------------------------------------------------------------
    # return:
    #   integer value indicating distance of first obstacle before the sensor.
    #   negative integer value if no obstacles is detected
    # 
    # parameter:
    #   location        -  [row, column]; location of sensor
    #   direction       -  char; direction where the sensor is facing to
    #   detect_range    -  max dist. the sensor can detect in a straight line
    # ----------------------------------------------------------------------
    def get_sensor_data(self, location, direction, detect_range):
        # print('detect_range:', detect_range)
        dis = 1
        if direction == 'E':
            # while (within boundary) and (block is free) and (not exceeding sensor range)
            while location[1]+dis < self.map_info.width \
                and self.map_info.isFree(location[0],location[1]+dis) \
                and dis <= detect_range:
                dis += 1
        elif direction == 'W':
            while location[1]-dis >= 0 \
                and self.map_info.isFree(location[0],location[1]-dis) \
                and dis <= detect_range:
                dis += 1
        elif direction == 'S':
            while location[0]+dis < self.map_info.height \
                and self.map_info.isFree(location[0]+dis,location[1]) \
                and dis <= detect_range:
                dis += 1
        elif direction == 'N':
            while location[0]-dis >= 0 \
                and self.map_info.isFree(location[0]-dis,location[1]) \
                and dis <= detect_range:
                dis += 1

        if dis > detect_range:
            # negative dis means not obstructed
            dis = -detect_range
        # verbose("    >> get_sensor_data; loc="+location + "; dir="+direction + "; ran="+detect_range + "; ret="+dis, tag='sensor')
        return dis
    # ----------------------------------------------------------------------

    def receive(self):
        data = [self.get_front_left(),
                self.get_front_right(),
                self.get_left(),
                self.get_right()]
        return data
    # ----------------------------------------------------------------------