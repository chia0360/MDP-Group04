# ----------------------------------------------------------------------
# class definition of Map.
# 
#   - self.arena:           2 dimensional array that defines the selected arena to be explored
#   - self.map:             2 dimensional array that defines the explored part of the map
#   - self.robot:           A pair of integers (x,y) that contains current position of robot (where x = Row & y = Cloumn)
#   - self.robot_direction: Direction of robot facing, 1 of either North, East, South, or West
# ----------------------------------------------------------------------

import config
import threading
from Arena import *
from logger import *
from map import *

class Map:
    ORIENTATION = ['N', 'E', 'S', 'W']

    def __init__(self):
        self.map_lock = threading.Lock()
<<<<<<< HEAD
        # ----------------------------------------------------------------------
        #   Map_real Legend:
        #       0 - free
        #       1 - obstacle
        # ----------------------------------------------------------------------
        self.__map_real =  [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [1, 1, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
=======

        #choose 1
        self.arena = Arena().a[0]
        self.arena = Arena().random_arena
>>>>>>> refs/remotes/origin/Joel
        
        # ----------------------------------------------------------------------
        #   Map Legend:
        #       0 - unexplored
        #       1 - explored; free
        #       2 - explored; obstacle
        # ----------------------------------------------------------------------
        self.map      =  [[1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1],
                            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1]]

        self.height     = config.map_detail['height']
        self.width      = config.map_detail['width']
        self.mapStat    = ['unexplored', 'free', 'obstacle']
        
        # Initialising Robot's location and the direction it is facing
        self.robot_location = [1, 1]
        self.robot_direction = 'E'


    # ----------------------------------------------------------------------
    #   Encapsulation functions
    # ----------------------------------------------------------------------
    def get_robot_location(self):
        return self.robot_location

    def get_robot_direction(self):
        return self.robot_direction

    def get_robot_direction_right(self):
        return Map.ORIENTATION[ (Map.ORIENTATION.index(self.robot_direction)+1) % 4 ]
    def get_robot_direction_left(self):
        return Map.ORIENTATION[ (Map.ORIENTATION.index(self.robot_direction)+3) % 4 ]
    def get_robot_direction_back(self):
        return Map.ORIENTATION[ (Map.ORIENTATION.index(self.robot_direction)+2) % 4 ]

    def set_robot_location(self, loc):
        if ((0 <= loc[0] < self.height) and
            (0 <= loc[1] < self.width )):
            self.robot_location = loc
        else:
            verbose( "Error: Location update out of range", tag="Map", lv='quiet' )

    def set_robot_direction(self, direction):
        if (direction in Map.ORIENTATION):
            self.robot_direction = direction
        else:
            verbose( "Error: Direction update invalid!", tag="Map", lv='quiet' )

    def set_map(self, y, x, stat):
        if not self.valid_range(y, x):
            verbose( "Warning: map to be set is out of bound!", tag="Map", lv='debug' )
            return

        if (stat in self.mapStat):
            self.map[y][x] = self.mapStat.index(stat)
        else:
            verbose( "Error: set map wrong status!", tag="Map", lv='quiet' )

    def get_map(self):
        return self.map

    def isSameMap(self, cmpmap):
        return cmpmap == self.map
    # ----------------------------------------------------------------------


    # ----------------------------------------------------------------------
    #   Function valid_pos
    # ----------------------------------------------------------------------
    # parameter:
    #   y   -   row position to be validated of robot
    #   x   -   coloumn position to be validated of robot
    # ----------------------------------------------------------------------
    def valid_pos(self, y, x):
        if not (0 < y < 14 and 0 < x < 19):
            return False
        for i in range(y-1, y+2):
            for j in range(x-1, x+2):
                if not self.valid_range(i,j) or self.isObstacle(i,j):
                    return False
        return True
    # ----------------------------------------------------------------------



    # ----------------------------------------------------------------------
    # map checking functions
    #     isExplored, isFree, isObstacle, valid_range
    # ----------------------------------------------------------------------
    # parameter:
    #     y, x    - row index and coloumn index respectively
    # ----------------------------------------------------------------------
    def isExplored(self, y, x):
        try:
            return (self.map[y][x] != 0)
        except IndexError:
            print(y,x,sep="; ")

    def isObstacle(self, y, x):
<<<<<<< HEAD
        if (self.__map[y][x] == 0):
            return self.__map_real[y][x] == 1
        return self.__map[y][x] == 2

    def isFree(self, y, x):
        verbose( "isFree({0},{1}): {2}; real:{3}".format(y,x,self.__map[y][x],self.__map_real[y][x]), lv='deepdebug' )
        if (self.__map[y][x] == 0):
            return self.__map_real[y][x] == 0
        return self.__map[y][x] == 1
=======
        if (self.map[y][x] == 0):
            return self.arena[y][x] == 1
        return self.map[y][x] == 2

    def isFree(self, y, x):
        verbose( "isFree({0},{1}): {2}; real:{3}".format(y,x,self.map[y][x],self.arena[y][x]), lv='deepdebug' )
        if (self.map[y][x] == 0):
            return self.arena[y][x] == 0
        return self.map[y][x] == 1
>>>>>>> refs/remotes/origin/Joel

    # to check whether the location is within range
    def valid_range(self, y, x):
        return (0 <= y < self.height) and (0 <= x < self.width)
    # ----------------------------------------------------------------------



    # ----------------------------------------------------------------------
    # Grading criteria functions
    #   map to be descripted need to be rotated 90 degrees clockwise
    # ----------------------------------------------------------------------
    def descripted_map(self, printThis=False, form='x'):
        part1 = 3           # the first '11'
        part2 = 3           # the second '11' - Part 1
        cnt   = 0           # part 2 bit counter for padding bit

        for x in range(self.width):
            for y in range(self.height):
                part1 <<= 1
                if (self.map[y][x] != 0) :
                    part1  |= 1
                    part2 <<= 1
                    cnt += 1
                    if (self.map[y][x] == 2):
                        part2 |= 1
        
        
        # Padding bits
        cnt      %= 8
        part2   <<= 8-cnt

        # Returning accoring format
        part1 = format(part1,form)
        part2 = format(part2,form)
        if printThis:
            print(part1, part2, sep=';\n')

        return [part1, part2]

    # ----------------------------------------------------------------------

#################### End of Class ####################
