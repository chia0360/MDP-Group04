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
        elif (algoName == "dum"):
            self.algo = algoDum()
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
        self.periodic_check(first_step=True)

    def periodic_check(self, first_step=False):

        if self.handler.get_robot_location() == [0, 0] and not first_step:
            return 

        if self.check_right():
            self.handler.right()
            self.handler.move()
        elif self.check_front():
            self.handler.move()
        else:
            # turn only
            self.handler.left()
        
        self.handler.simulator.master.after(500, self.periodic_check)

    def findSP(self):
        pass

    def run(self):
        pass

    def check_right(self):
        # robot location is always the block in top left corner of the robot
        robot_location = self.handler.map.get_robot_location()
        robot_right_direction = self.handler.map.get_robot_direction_right()
        current_map = self.map.get_map()

        if robot_right_direction == 'N':
            # right is north but the top left corner is already at row 0 so cannot move north
            if robot_location[0] <= 0:
                return False
            # the 2 blocks up north free
            if current_map[robot_location[0]-1][robot_location[1]] == 1 and \
                current_map[robot_location[0]-1][robot_location[1]+1] == 1:
                return True
            # if there are still unexplored blocks to the right, turn to explore first
            elif current_map[robot_location[0]-1][robot_location[1]] == 0 or \
                current_map[robot_location[0]-1][robot_location[1]+1] == 0:
                self.handler.right()
                # need to turn back before return
                if self.check_front():
                    self.handler.left()
                    return True
                else:
                    self.handler.left()
                    return False
        elif robot_right_direction == 'S':
            # right is south but the top left corner is already at row 13 (15-2),
            # so bottom of robot is at row 14 so cannot move south
            if robot_location[0] >= self.map.height-2:
                return False
            # the 2 blocks south free
            if current_map[robot_location[0]+2][robot_location[1]] == 1 and \
                current_map[robot_location[0]+2][robot_location[1]+1] == 1:
                return True
            elif current_map[robot_location[0]+2][robot_location[1]] == 0 or \
                current_map[robot_location[0]+2][robot_location[1]+1] == 0:
                self.handler.right()
                # need to turn back before return
                if self.check_front():
                    self.handler.left()
                    return True
                else:
                    self.handler.left()
                    return False
        elif robot_right_direction == 'E':
            if robot_location[1] >= self.map.width-2:
                return False
            # the 2 blocks east free
            if current_map[robot_location[0]][robot_location[1]+2] == 1 and \
                current_map[robot_location[0]+1][robot_location[1]+2] == 1:
                return True
            elif current_map[robot_location[0]][robot_location[1]+2] == 0 or \
                current_map[robot_location[0]+1][robot_location[1]+2] == 0:
                self.handler.right()
                # need to turn back before return
                if self.check_front():
                    self.handler.left()
                    return True
                else:
                    self.handler.left()
                    return False
        elif robot_right_direction == 'W':
            if robot_location[1] <= 0:
                return False
            if current_map[robot_location[0]][robot_location[1]-1] == 1 and \
                current_map[robot_location[0]+1][robot_location[1]-1] == 1:
                return True
            elif current_map[robot_location[0]][robot_location[1]-1] == 0 or \
                current_map[robot_location[0]+1][robot_location[1]-1] == 0:
                self.handler.right()
                # need to turn back before return
                if self.check_front():
                    self.handler.left()
                    return True
                else:
                    self.handler.left()
                    return False
        else:
            print("[Error] Invalid direction.")

    def check_front(self):
        sensor_data = self.handler.robot.receive()
        print('Sensor data: ', sensor_data)
        # sensor data [front left, front right, left, right]

        # more than 1 means there are still room infront, less than 0 means the distance is more than the sensor's limit
        if (sensor_data[0] > 1 or sensor_data[0] < 0) and \
           (sensor_data[1] > 1 or sensor_data[1] < 0):
            return True
        else:
            return False