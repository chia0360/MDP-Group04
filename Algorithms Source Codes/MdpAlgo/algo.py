# ----------------------------------------------------------------------
# class definition of algoAbstract.
# 
#   - explore()
#		robot starts doing exploration
# 
#   - findSP()
#		Finding Shortest Path, based on the known maps.
# 
#   - run()
#		robot starts running according shortest path algorithm
# ----------------------------------------------------------------------

import time
import mapclass
from math import *
import descriptor
import config

class algoAbstract:
    # def __init__(self):

    def explore(self):
        raise NotImplementedError

    def findSP(self):
        raise NotImplementedError

    def run(self):
        raise NotImplementedError


# ----------------------------------------------------------------------
class algoDum(algoAbstract):
    def explore(self):
        pass
    def findSP(self):
        pass
    def run(self):
        pass
# ----------------------------------------------------------------------


# ----------------------------------------------------------------------
# class definition of algoFactory.
# 
#   - explore()
#		robot starts doing exploration
# 
#   - findSP()
#		Finding Shortest Path, based on the known maps.
# 
#   - run()
#		robot starts running according shortest path algorithm
# ----------------------------------------------------------------------
class algoFactory:
    def __init__(self, handler, algoName="RHR"):
        if (algoName == "BF1"):
            self.algo = algoBF1(handler)
        elif (algoName == 'RHR'):
            self.algo = RightHandRule(handler)
        else:
            raise NameError('algoName not found')

    def explore(self):
        self.algo.explore()

    def findSP(self):
        self.algo.findSP()

    def run(self):
        self.algo.run()
        

# ----------------------------------------------------------------------
# class definition of algoBF1.
# Implementation class of algoAbstract using algorithm Brute Force #1
# ----------------------------------------------------------------------
class algoBF1(algoAbstract):
    def __init__(self, handler):
        self.handler    = handler
        self.map        = handler.map
        self.simulator = handler.simulator
        self.ending_moves = []
        # this steps contain a list of step taken from the original position to the current position
        # data structure of stepsTaken:
        # in each item of the list, we have
        # [previousMove, currentPosition, ]
        self.stepsTaken = []
        # done is used to stop the bruteforce algo early and make the robot return to original posision
        self.done = False
        # ensure the the goal is reached
        self.goal_reached = False
        # when a move is taken from a position, it is recorded so that that move will not be taken again
        # key is position (tuple), and the value is a list of direction it has done.
        self.movesLeft = {}
        self.interval = 40
        self.shortest_path_moves = []

        self.astar = AStar()

        # we initialize the first row, last row, first col, last col because for example, the first row cannot move north.
        for row in range(1, 14):
            for col in range(1, 19):
                self.movesLeft[(row, col)] = ['N', 'S', 'E', 'W']

        # first row, last row
        for col in range(1, 19):
            self.movesLeft[(1, col)].remove('N')
            self.movesLeft[(13, col)].remove('S')

        # first col, last col
        for row in range(1, 14):
            self.movesLeft[(row, 1)].remove('W')
            self.movesLeft[(row, 18)].remove('E')
        print("Init movesLeft", self.movesLeft[(1,1)])

    def explore(self):
        self.start_time = time.time()
        self.end_time = self.simulator.specified_time()
        self.periodic_check()

    def check_complete(self):
        explored_map = self.map.get_map()
        for i in range(0, 15):
            for j in range(0, 20):
                if explored_map[i][j] == 0:
                    return False
        # print the map
        for i in range(1, 14):
            print(explored_map[i])
        return True

    def periodic_check(self):
        print("calling periodic_check")
        # Speed Set(no. of steps/sec)
        self.simulator.specified_speed()
        if (self.simulator.speed_status == True):
            time.sleep(1/int(self.simulator.speed.get()))

        # Coverage Figure Set (%)
        self.simulator.specified_coverage()
        cov = int(self.simulator.coverage.get())
        if (self.simulator.coverage_status == True):
            print(self.map.countExplored())
            print(self.map.mapSize)
            div = self.map.countExplored()/self.map.mapSize
            if(div*100 >= cov):
                #Return to start
                self.return_to_start()
                return

        # Time Set(min:sec)
        if (self.simulator.time_status == True):
            if (float(self.end_time) <= (time.time()-self.start_time)):
                #add return to start
                self.return_to_start()
                #end of test
                return

        # check the movesLeft for currentPosition
        self.currentPosition = tuple(self.handler.map.get_robot_location())
        movesAvailable = self.movesLeft[self.currentPosition]
        if self.currentPosition == (13, 18):
            self.goal_reached = True
        # early stopping 
        # check if all the blocks are explored
        if self.check_complete():
            print("done")
            
            # check if the goal is reached
            if self.goal_reached:
                # return to start
                self.return_to_start()
                return
            else:
                # go to goal then return to start
                currentPos = tuple(self.handler.map.get_robot_location())
                self.ending_moves = self.astar.solve(self.map.get_map(), currentPos, self.astar.goal)
                self.ending_moves.extend(self.astar.solve(self.map.get_map(), self.astar.goal, self.astar.start))
                self.handler.simulator.master.after(self.interval, self.ending)
                return

        # if no more movesAvailable for the current position, take a step backward
        # last item in the stepsTaken has [move, position]
        # turn the robot to the direction of the move previously taken and then take a step backward
        if len(movesAvailable) == 0:
            move = self.stepsTaken[-1][0]
            # turn right until the robot is facing in the direction to move
            while move != self.handler.map.get_robot_direction():
                print(move, self.handler.map.get_robot_direction())
                self.handler.right()
            # take backward step
            self.handler.back()
            # delete the step in stepsTaken
            self.stepsTaken.pop()
            # if the robot cannot handle moving backward, we need to implement this differently at the later time
        else:
            # take one available moves
            move = movesAvailable.pop()

            # turn right until the robot is facing in the direction to move
            while move != self.handler.map.get_robot_direction():
                print(move, self.handler.map.get_robot_direction())
                self.handler.right()

            # then take a step forward if possible
            if self.check_front():
                self.handler.move()

                # remove the backward move from the nextPosition
                nextPosition = tuple(self.handler.map.get_robot_location())
                if move == 'N':
                    backward = 'S'
                elif move == 'S':
                    backward = 'N'
                elif move == 'E':
                    backward = 'W'
                else:
                    backward = 'E'
                self.movesLeft[nextPosition].remove(backward)

                # record the step will be taken
                self.stepsTaken.append([move, self.currentPosition])
            # if not we just don't move and wait for next iteration
            
        self.handler.simulator.master.after(self.interval, self.periodic_check)

    def findSP(self):
        # use the generic astar to find the shortest path
        self.shortest_path_moves = self.astar.solve(self.map.get_map(), self.astar.start, self.astar.goal)
        print(self.shortest_path_moves)

    def run(self):
        # have not found the shortest path, run findSP to find
        if not self.shortest_path_moves:
            self.findSP()
        direction = self.shortest_path_moves.pop(0)
        self.moveTo(direction)
        # still have moves left to go
        if self.shortest_path_moves:
            self.handler.simulator.master.after(self.interval, self.run)

    def check_front(self):
        sensor_data = self.handler.robot.receive()
        print('Sensor data: ', sensor_data)
        if (sensor_data[0] > 1 or sensor_data[0] < 0) and \
            (sensor_data[1] > 1 or sensor_data[1] < 0) and \
            (sensor_data[2] > 1 or sensor_data[2] < 0):
            return True
        else:
            return False

    def ending(self):
        # start doing the ending moves
        direction = self.ending_moves.pop(0)
        self.moveTo(direction)
        if len(self.ending_moves) > 0:
            self.handler.simulator.master.after(self.interval, self.ending)


    def moveTo(self, directions):
        for direction in directions:
            print("moving to", direction)
            
            if self.handler.map.get_robot_direction() == direction:
                self.handler.move()
            elif self.handler.map.get_robot_direction_right() == direction:
                self.handler.right()
                self.handler.move()
            elif self.handler.map.get_robot_direction_left() == direction:
                self.handler.left()
                self.handler.move()
            else:
                self.handler.left()
                self.handler.left()
                self.handler.move()
    
    def return_to_start(self):
        currentPos = tuple(self.handler.map.get_robot_location())
        if currentPos == (1,1):
            return
        self.ending_moves = self.astar.solve(self.map.get_map(), currentPos, self.astar.start)
        self.handler.simulator.master.after(self.interval, self.ending)


class RightHandRule(algoAbstract):
    def __init__(self, handler):
        self.handler    = handler
        self.map        = handler.map
        self.shortest_path_moves = []
        self.done = False
        self.interval = 20
        self.m = mapclass.Map()
        self.des = descriptor.descriptor()
        self.real = config.robot_simulation

    def explore(self):
        # periodic check is for the simulation
        if self.done:
            return
        self.periodic_check()
        # for real run just call this once when receive the command

    def periodic_check(self):
        # print("periodic check")
        if self.check_right():
            print("right free, turing right")
            # turning and moving is already done
            if not self.real:
                self.handler.simulator.master.after(self.interval, self.periodic_check)
            return

        if self.check_front():
            print("front free, moving front")
            self.handler.move()
        else:
            print("left free, moving left")
            self.handler.left()
        
        location = self.handler.map.get_robot_location()
        print("robot location", location)
        if location[0] == 1 and location[1] == 1:
            self.done = True
            
        if not self.done and not self.real:
            self.handler.simulator.master.after(self.interval, self.periodic_check)
            
#print Descriptor with every move
        explored = self.map.get_map()
        self.des.map = explored
        # a = self.des.descriptor1()
        # b = self.des.descriptor2()
        # print("end periodic_check")
        
    def findSP(self):
        # use the generic astar to find the shortest path
        astar = AStar()
        self.shortest_path_moves = astar.solve(self.map.get_map(), astar.start, astar.goal)
        print(self.shortest_path_moves)
        return self.shortest_path_moves

    def run(self):
        # have not found the shortest path, run findSP to find
        if not self.shortest_path_moves:
            self.findSP()
        direction = self.shortest_path_moves.pop(0)
        self.moveTo(direction)
        # still have moves left to go
        if self.shortest_path_moves:
            self.handler.simulator.master.after(self.interval, self.run)

    def moveTo(self, directions):
        for direction in directions:
            print("moving to", direction)
            
            if self.handler.map.get_robot_direction() == direction:
                self.handler.move()
            elif self.handler.map.get_robot_direction_right() == direction:
                self.handler.right()
                self.handler.move()
            elif self.handler.map.get_robot_direction_left() == direction:
                self.handler.left()
                self.handler.move()
            else:
                self.handler.left()
                self.handler.left()
                self.handler.move()

    def check_right(self):
        print("start check right")
        robot_location = self.handler.map.get_robot_location()
        right_direction = self.handler.map.get_robot_direction_right()
        map_explored = self.map.get_map()
        print ("robot location", robot_location)
        
        if right_direction == 'N':
            # already touching the wall
            if robot_location[0] <= 1:
                print("touching north")
                return False
            # ensure the 3 blocks have been explore, if not turn to explore them
            # 0 means not explored

            # define the y, x location of the blocks on the right of the robot
            y1 = robot_location[0]-2
            y2 = robot_location[0]-2
            y3 = robot_location[0]-2
            x1 = robot_location[1] 
            x2 = robot_location[1]-1
            x3 = robot_location[1]+1
            
        elif right_direction == 'S':
            if robot_location[0] >= self.map.width - 2:
                print("touching south")
                return False

            y1 = robot_location[0]+2
            y2 = robot_location[0]+2
            y3 = robot_location[0]+2
            x1 = robot_location[1] 
            x2 = robot_location[1]-1
            x3 = robot_location[1]+1

        elif right_direction == 'E':
            if robot_location[1] >= self.map.length - 2:
                print("touching east")
                return False

            y1 = robot_location[0]
            y2 = robot_location[0]+1
            y3 = robot_location[0]-1
            x1 = robot_location[1]+2 
            x2 = robot_location[1]+2
            x3 = robot_location[1]+2    

        elif right_direction == 'W':
            if robot_location[1] <= 1:
                print("touching west")
                return False

            y1 = robot_location[0]
            y2 = robot_location[0]+1
            y3 = robot_location[0]-1
            x1 = robot_location[1]-2 
            x2 = robot_location[1]-2
            x3 = robot_location[1]-2    

        else:
            print("[Error] Invalid direction.")
            return False

        # set this variable to check if the robot needed to turn to explore, we use this to decide whether we need to turn back
        # turned = False

        # common logic
        # check if the blocks on the robot's right are explored, if not explore then turn right to explore those
        # if map_explored[y1][x1] == 0 or \
        #     map_explored[y2][x2] == 0 or \
        #     map_explored[y3][x3] == 0:
        #     self.handler.right()
        #     # wait for robot to turn then we read the map
        #     time.sleep(1)
        #     self.handler.do_read()
        #     self.handler.simulator.update_map()
        #     turned = True

        # now check if all those blocks are free
        # print("checking blocks on the right are free")
        # we can assume all blocks on the right are explored
        # print()
        if map_explored[y1][x1] == 1 and \
            map_explored[y2][x2] == 1 and \
            map_explored[y3][x3] == 1:
            # print("they are free")
            # no need to turn back
            # move forward 1 step return True
            # if not turned:
                # haven't turned because map already explored robot didn't need to turn to explore the map
                # so robot need to turn now
            self.handler.right()
            self.handler.move()
            return True
        else:
            # if turned:
                # turn back
                # self.handler.left()
            return False
        

    def check_front(self):
        data = self.handler.robot.receive()

        # the loop to wait for sensor is here
        while not data:
            # this sensor data is in the the following order
            data = self.handler.robot.receive()
            # left,         front-left, front-middle, front-right, right for real data
            # front_middle, front-left, front-right,  left,        right for simulation
        
        sensor_data = data

        print('Sensor data: ', sensor_data)
        if (sensor_data[0] > 1 or sensor_data[0] < 0) and \
            (sensor_data[1] > 1 or sensor_data[1] < 0) and \
            (sensor_data[2] > 1 or sensor_data[2] < 0):
            return True
        else:
            return False

class AStar:
    """
    Pass in a map, an origin and a destination to get back the list of moves (in 4 directions) for the shortest path 
    """
    def __init__(self):
        self.start = (1,1)
        self.goal = (13, 18)
        self.side_cost = 10
        self.diagonal_cost = 14
        pass
    
    def distance(self, position1, position2):
        # this act as our heuristics function
        # here we don't straight use the euclidean distance
        # but a more reasonable estimate
        d1 = position1[0]-position2[0]
        d2 = position1[1]-position2[1]
        # make d1 the smaller number
        if d1 > d2:
            d1, d2 = d2, d1
        diff = d2 - d1
        dist = diff * 14 + d1 * 10
        return dist

    def solve(self, map, origin, dest):
        # make a copy of the map
        local_map = [row[:] for row in map]

        #-----Preprocessing of the map start----

        # if the map is not 100% explored due in case of using RightHandRule
        # assume all those unexplored tiles are blocked
        for i in range(20):
            for j in range(15):
                if local_map[j][i] == 0:
                    local_map[j][i] = 2
    
        # create a bounding box for all the obstacles and wall
        # use number 3 to indicate bounding box
        # for the wall
        for i in range(20):
            # row 0
            if local_map[0][i] != 2:
                local_map[0][i] = 3
            # row 14
            if local_map[14][i] != 2:
                local_map[14][i] = 3

        for i in range(15):
            # col 0
            if local_map[i][0] != 2:
                local_map[i][0] = 3
            if local_map[i][19] != 2:
                local_map[i][19] = 3
            
        # for each obstacles
        for i in range(20):
            for j in range(15):
                # turn the 8 surrounding blocks of the current block to 3 if the block is 2
                if local_map[j][i] == 2:
                    # top
                    if j > 0 and local_map[j-1][i] == 1:
                        local_map[j-1][i] = 3
                    # top right
                    if j > 0 and i < 19 and local_map[j-1][i+1] == 1:
                        local_map[j-1][i+1] = 3
                    # top left
                    if j > 0 and i > 0 and local_map[j-1][i-1] == 1:
                        local_map[j-1][i-1] = 3                   
                    # bottom
                    if j < 14 and local_map[j+1][i] == 1:
                        local_map[j+1][i] = 3
                    # bottom right
                    if j < 14 and i < 19 and local_map[j+1][i+1] == 1:
                        local_map[j+1][i+1] = 3
                    # bottom left
                    if j < 14 and i > 0 and local_map[j+1][i-1] == 1:
                        local_map[j+1][i-1] = 3
                    # left
                    if i > 0 and local_map[j][i-1] == 1:
                        local_map[j][i-1] = 3
                    # right
                    if i < 19 and local_map[j][i+1] == 1:
                        local_map[j][i+1] = 3
                    

        #----Preprocessing of the map is completed, only those blocks numbered 1 is movable-----

        #----The actual A* algorithms----

        # cost from the origin to the node
        gScore = {}
        # cost from start to start is 0
        gScore[origin] = 0
        # every time we move to a neighbor node, we 
        # increase the gScore of the neighbor by 10 
        # if its on the sides, if its on the diagonal,
        # increase by 14

        # the open list contains the nodes to be evaluated
        # as key as the fScore of the node as value
        open_list = {}
        # here the origin to destination we use the distance
        # directly since the gScore is 0
        open_list[origin] = self.distance(origin, dest)
        closed_list = []
        came_from = {}
        # list of node that have not been expanded

        while len(open_list) != 0:
            # current node is the node in the open list with lowest fScore
            current = min(open_list, key=open_list.get)
            # remove the current node from open list
            open_list.pop(current)

            # add current node to closed list
            closed_list.append(current)

            # if current equal dest, we are done
            if current == dest:
                break

            # open up the surrounding nodes
            
            # if the neighbor is not in closed_list, not in open_list, and traversable, we add it into open_list 
            # with calculated fScore
            
            y, x = current
            # top 
            top =  (y-1, x)
            if local_map[top[0]][top[1]] == 1 and top not in closed_list:
                # fScore is the cost from start + estimated heuristics 
                # cost to end
                # the cost from start will equal the cost from start
                # of the previous node + either 10 or 14 depends 
                # on the position
                fScore = gScore[current] + self.side_cost + self.distance(top, dest)
                tentative_gScore = gScore[current] + self.side_cost
                if top not in open_list or tentative_gScore < gScore[top]:
                    open_list[top] = fScore
                    gScore[top] = tentative_gScore
                    came_from[top] = current
                    # best until now or new node

            # bottom 
            bottom =  (y+1, x)
            if local_map[bottom[0]][bottom[1]] == 1 and bottom not in closed_list:
                fScore = gScore[current] + self.side_cost + self.distance(bottom, dest)
                tentative_gScore = gScore[current] + self.side_cost
                if bottom not in open_list or tentative_gScore < gScore[bottom]:
                    came_from[bottom] = current
                    gScore[bottom] = tentative_gScore
                    open_list[bottom] = fScore

            # left 
            left =  (y, x-1)
            if local_map[left[0]][left[1]] == 1 and left not in closed_list:
                fScore = gScore[current] + self.side_cost + self.distance(left, dest)
                tentative_gScore = gScore[current] + self.side_cost
                if left not in open_list or tentative_gScore < gScore[left]:
                    came_from[left] = current
                    gScore[left] = tentative_gScore
                    open_list[left] = fScore

            # right 
            right =  (y, x+1)
            if local_map[right[0]][right[1]] == 1 and right not in closed_list:
                fScore = gScore[current] + self.side_cost + self.distance(right, dest)
                tentative_gScore = gScore[current] + self.side_cost
                if right not in open_list or tentative_gScore < gScore[right]:
                    came_from[right] = current
                    gScore[right] = tentative_gScore
                    open_list[right] = fScore
            
            # now for the diagonal blocks
            # we also test like above + test if the move is possible
            # for example if we want to move to top right
            # we need to check if top and right blocks are traversable 
            # topright 
            topright =  (y-1, x+1)
            if local_map[topright[0]][topright[1]] == 1 and topright not in closed_list:
                # check moveable
                if local_map[right[0]][right[1]] == 1 and local_map[top[0]][top[1]] == 1:
                    fScore = gScore[current] + self.diagonal_cost + self.distance(topright, dest)
                    tentative_gScore = gScore[current] + self.diagonal_cost
                    if topright not in open_list or tentative_gScore < gScore[topright]:
                        came_from[topright] = current
                        gScore[topright] = tentative_gScore
                        open_list[topright] = fScore

            # topleft 
            topleft =  (y-1, x-1)
            if local_map[topleft[0]][topleft[1]] == 1 and topleft not in closed_list:
                # check moveable
                if local_map[left[0]][left[1]] == 1 and local_map[top[0]][top[1]] == 1:
                    fScore = gScore[current] + self.diagonal_cost + self.distance(topleft, dest)
                    tentative_gScore = gScore[current] + self.diagonal_cost
                    if topleft not in open_list or tentative_gScore < gScore[topleft]:
                        came_from[topleft] = current
                        gScore[topleft] = tentative_gScore
                        open_list[topleft] = fScore

            # bottom right 
            bottomright =  (y+1, x+1)
            if local_map[bottomright[0]][bottomright[1]] == 1 and bottomright not in closed_list:
                # check moveable
                if local_map[right[0]][right[1]] == 1 and local_map[bottom[0]][bottom[1]] == 1:
                    fScore = gScore[current] + self.diagonal_cost + self.distance(bottomright, dest)
                    tentative_gScore = gScore[current] + self.diagonal_cost
                    if bottomright not in open_list or tentative_gScore < gScore[bottomright]:
                        came_from[bottomright] = current
                        gScore[bottomright] = tentative_gScore
                        open_list[bottomright] = fScore
            
            # bottom left 
            bottomleft =  (y+1, x-1)
            if local_map[bottomleft[0]][bottomleft[1]] == 1 and bottomleft not in closed_list:
                # check moveable
                if local_map[left[0]][left[1]] == 1 and local_map[bottom[0]][bottom[1]] == 1:
                    fScore = gScore[current] + self.diagonal_cost + self.distance(bottomleft, dest)
                    tentative_gScore = gScore[current] + self.diagonal_cost
                    if bottomleft not in open_list or tentative_gScore < gScore[bottomleft]:
                        came_from[bottomleft] = current
                        gScore[bottomleft] = tentative_gScore
                        open_list[bottomleft] = fScore

        # found the path, now just need to print the path from the dest node to the origin node

        result = [dest]

        node = came_from[dest]
        while True:
            result.insert(0, node)
            if node in came_from:
                node = came_from[node]
                continue
            else:
                break

        # result now has the list of tiles to traverse on

        # we need to convert them to a list of moves in ['N', 'S', 'E', 'W', 'NE', 'NW', 'SE', 'SW']
        # print("map")
        # for row in local_map: 
        #     print(row)
        # print("result", result)
        moves = []
        for i in range(len(result)-1):
            if result[i][0] < result[i+1][0]:
                if result[i][1] == result[i+1][1]:
                    moves.append('S')
                elif result[i][1] > result[i+1][1]:
                    moves.append('SW')
                else:
                    moves.append('SE')
            elif result[i][0] > result[i+1][0]:
                if result[i][1] == result[i+1][1]:
                    moves.append('N')
                elif result[i][1] > result[i+1][1]:
                    moves.append('NW')
                else:
                    moves.append('NE')
            else:
                if result[i][1] < result[i+1][1]:
                    moves.append('E')
                else:
                    moves.append('W')
        # print(moves)
        return moves
