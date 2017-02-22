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

        #choose 1
        arena = Arena()
        arena.load("arena_test")
        self.arena = arena.loaded_arena

        #for row in self.arena:
        #    print(row)
        # ----------------------------------------------------------------------
        #   Map Legend:
        #       0 - unexplored
        #       1 - explored; free
        #       2 - explored; obstacle
        # ----------------------------------------------------------------------
        self.map      =  [
                            [1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
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

        self.width     = config.map_dimensions['width']
        self.length      = config.map_dimensions['length']
        self.mapSize    = self.length * self.width
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
        if ((0 <= loc[0] < self.width) and
            (0 <= loc[1] < self.length )):
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
    #     isExplored, isFree, isObstacle, countExplored, valid_range
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
        if (self.map[y][x] == 0):
            return self.arena[y][x] == 1;
        else:
            return self.map[y][x] == 2

    def isFree(self, y, x):
        verbose( "isFree({0},{1}): {2}; real:{3}".format(y,x,self.map[y][x],self.arena[y][x]), lv='deepdebug' )
        if (self.map[y][x] == 0):
            return self.arena[y][x] == 0;
        else:
            return self.map[y][x] == 1

    def countExplored(self):
        unexplored_cells = 0
        for y in range (0,self.width):
            for x in range (0,self.length):
                if (self.map[y][x] !=0):
                    unexplored_cells += 1
        return unexplored_cells
                
    # to check whether the location is within range
    def valid_range(self, y, x):
        return (0 <= y < self.width) and (0 <= x < self.length)
    # ----------------------------------------------------------------------



    # ------------------------------------------------------------------------------------------
    # Generate map descriptor
    # descriptor1: Mark each unexplored square as 0 and each explored square as 1
    # descriptor2: Only grid cells marked as “explored” in Part 1 are represented here by a bit.
    # Mark cells known to be empty space with 0, mark cells known to contain an obstacle with 1
    # -------------------------------------------------------------------------------------------

    def descriptor1(self):
        print(self.map)
        rotated = list(zip(*(self.map)))[::-1]
        print(rotated)
        ret = "11" #padded
        for i in range (19,0,-1):
            for j in range(15):
               ret += str(rotated[i][j])
        ret += "11" #padded
        hexa = ""
        for i in range(0,len(ret),4):
            temp = ""
            temp += ret[i:i+1]
            temp += ret[i+1:i+2]
            temp += ret[i+2:i+3]
            temp += ret[i+3:i+4]
            hexa += str(hex(int(temp,2)))[2:3]
        print(hexa)
                
    def descriptor2(self):
        print(self.map)
        rotated = list(zip(*(self.map)))[::-1]
        print(rotated)
        ret = ""
        cnt = 0
        for i in range (19,0,-1):
            for j in range(15):
                if rotated[i][j] > 0:
                    cnt += 1
                    if (rotated[i][j] == 1):      #Explored, free: Mark as 0
                        ret += "0"
                    elif (rotated[i][j] == 2):    #Explored, obstacle: Mark as 1
                        ret += "1"
        
        while cnt % 8 != 0:
            ret += "0"
            cnt += 1
        print(ret)
            
        hexa = ""
        for i in range(0,len(ret),4):
            temp = ""
            temp += ret[i:i+1]
            temp += ret[i+1:i+2]
            temp += ret[i+2:i+3]
            temp += ret[i+3:i+4]
            hexa += str(hex(int(temp,2)))[2:3]
        print(hexa)
    # ----------------------------------------------------------------------

#################### End of Class ####################
