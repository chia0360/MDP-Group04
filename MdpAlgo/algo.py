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

    def explore(self):
        # robot_location  = self.map.get_robot_location()
        self.periodic_check()

    def periodic_check(self):
        self.handler.move()
        self.handler.simulator.master.after(500, self.periodic_check)

    def findSP(self):
        pass

    def run(self):
        pass


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