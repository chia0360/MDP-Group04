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
        # check if the goal is reached
        print("steps taken", self.stepsTaken)
        currentPosition = tuple(self.handler.map.get_robot_location())
        # check the movesLeft for currentPosition
        movesAvailable = self.movesLeft[currentPosition]

        if currentPosition == (13, 18):
            self.goal_reached = True
        # early stopping 
        # check if all the blocks are explored
        if self.check_complete():
            print("done")
            if self.goal_reached:
                # return to start
                return
            else:
                # go to goal then return to start
                return

        # if no more movesAvailable for the current posision, take a step backward
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
                self.stepsTaken.append([move, currentPosition])
            # if not we just don't move and wait for next iteration
            
        self.handler.simulator.master.after(10, self.periodic_check)

    def findSP(self):
        pass

    def run(self):
        pass

    def check_front(self):
        sensor_data = self.handler.robot.receive()
        print('Sensor data: ', sensor_data)
        if (sensor_data[0] > 1 or sensor_data[0] < 0) and \
            (sensor_data[1] > 1 or sensor_data[1] < 0) and \
            (sensor_data[2] > 1 or sensor_data[2] < 0):
            return True
        else:
            return False


class RightHandRule(algoAbstract):
    def __init__(self, handler):
        self.handler    = handler
        self.map        = handler.map

    def explore(self):
        self.periodic_check()

    def periodic_check(self):
        if self.check_right():
            # turning and moving is already done
            self.handler.simulator.master.after(200, self.periodic_check)
            return

        if self.check_front():
            self.handler.move()
        else:
            self.handler.left()
        self.handler.simulator.master.after(200, self.periodic_check)

    def findSP(self):
        pass

    def run(self):
        pass

    def check_right(self):
        robot_location = self.handler.map.get_robot_location()
        right_direction = self.handler.map.get_robot_direction_right()
        map_explored = self.map.get_map()
        if right_direction == 'N':
            # already touching the wall
            if robot_location[0] <= 1:
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
            if robot_location[0] >= self.map.height - 2:
                return False

            y1 = robot_location[0]+2
            y2 = robot_location[0]+2
            y3 = robot_location[0]+2
            x1 = robot_location[1] 
            x2 = robot_location[1]-1
            x3 = robot_location[1]+1

        elif right_direction == 'E':
            if robot_location[1] >= self.map.width - 2:
                return False

            y1 = robot_location[0]
            y2 = robot_location[0]+1
            y3 = robot_location[0]-1
            x1 = robot_location[1]+2 
            x2 = robot_location[1]+2
            x3 = robot_location[1]+2    

        elif right_direction == 'W':
            if robot_location[1] <= 2:
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
        turned = False

        # common logic
        # check if the blocks on the robot's right are explored, if not explore then turn right to explore those
        if map_explored[y1][x1] == 0 or \
            map_explored[y2][x2] == 0 or \
            map_explored[y3][x3] == 0:
            self.handler.right()
            turned = True

        # now check if all those blocks are free
        if map_explored[y1][x1] == 1 and \
            map_explored[y2][x2] == 1 and \
            map_explored[y3][x3] == 1:
            # no need to turn back
            # move forward 1 step return True
            if not turned:
                # haven't turned because map already explored robot didn't need to turn to explore the map
                # so robot need to turn now
                self.handler.right()
            self.handler.move()
            return True
        else:
            if turned:
                # turn back
                self.handler.left()
            return False
        

    def check_front(self):
        sensor_data = self.handler.robot.receive()
        print('Sensor data: ', sensor_data)
        if (sensor_data[0] > 1 or sensor_data[0] < 0) and \
            (sensor_data[1] > 1 or sensor_data[1] < 0) and \
            (sensor_data[2] > 1 or sensor_data[2] < 0):
            return True
        else:
            return False
