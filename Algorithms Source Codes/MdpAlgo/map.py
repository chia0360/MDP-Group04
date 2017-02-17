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

        for row in self.arena:
            print(row)
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

        self.height     = config.map_detail['height']
        self.width      = config.map_detail['width']
        self.mapSize    = self.height * self.width
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
        for y in range (0,self.height):
            for x in range (0,self.width):
                if (self.map[y][x] !=0):
                    unexplored_cells += 1
        return unexplored_cells
                
    # to check whether the location is within range
    def valid_range(self, y, x):
        return (0 <= y < self.height) and (0 <= x < self.width)
    # ----------------------------------------------------------------------




    # ----------------------------------------------------------------------
    # Generate map descriptor
    # ----------------------------------------------------------------------
    
    def descriptor_one(self):                   #Mark each unexplored square as 0 and each explored square as 1.
        rotated = list(zip(*(self.map)))[::-1]  #rotate map 90 degrees counterclockwise

        ret = [1, 1]    #Padding for beginning
        for row in rotated:
            for col in row:
                if col > 0:
                    ret.append(1)
                else:
                    ret.append(0)
                    
        ret.append(1)
        ret.append(1)   #Padding for ending

        
        #print(ret)
        
        hex_ret = []
        temp = []
        for bit in ret:
            if len(temp) < 4:
                temp.append(bit)
            else:
                temp_str = ''.join([str(b) for b in temp])
                hex_ret.append(str(hex(int(temp_str, 2)))[2:])
                temp = [bit]
        if len(temp) > 0:
            temp_str = ''.join([str(b) for b in temp])
            hex_ret.append(str(hex(int(temp_str, 2)))[2:])
        
        #print(hex_ret)
        # print(len(hex_ret))

        return ''.join([h for h in hex_ret])        #  converting to hexadecimal for display

    #Part 2
    
    def descriptor_two(self):
        rotated = list(zip(*(self.map)))[::-1]  #rotate map 90 degrees counterclockwise
        ret = []
        cnt = 0
        for row in rotated:
            for col in row:
                if col > 0:
                    cnt += 1
                    if col == 2:    # grid cells marked as “explored” are represented by a bit, and obstacles are represented by 1
                        ret.append(1)
                    else:           # Cells that are known to be empty space are marked with a 0
                        ret.append(0)
        while cnt % 8 != 0:
            ret.append(0)
            cnt += 1
            
        #print(ret)
        # print(len(ret))
        hex_ret = []
        temp = []
        for bit in ret:
            if len(temp) < 4:
                temp.append(bit)
            else:
                temp_str = ''.join([str(b) for b in temp])
                hex_ret.append(str(hex(int(temp_str, 2)))[2:])
                temp = [bit]
        if len(temp) > 0:
            temp_str = ''.join([str(b) for b in temp])
            hex_ret.append(str(hex(int(temp_str, 2)))[2:])
            
        #print(hex_ret)
        # print(len(hex_ret))

        print( ''.join([h for h in hex_ret]))
    # ----------------------------------------------------------------------

#################### End of Class ####################
