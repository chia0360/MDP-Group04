from Map import *
from Node import *
from Cell import *

class Robot:
        
        def __init__(self):
                self.X = 1
                self.Y = 1
                self.Range = 1
                self.Dir = 'U'
                "empty memory for robot"
                self.Memory = Map(15,20)
                self.XGoal = 13
                self.YGoal = 18
                self.XStart = 1
                self.YStart = 1
                self.turnedRight = False
                self.turnedAround = False
                self.turnedLeft = False
                self.StartNode = Node(self.XStart, self.YStart)
                self.GoalNode = Node(self.XGoal, self.YGoal)
                "self.ShortestPath = Node[]"
                self.enteredGoal=False
                self.mapStr = ''

        def __init__(self, x, y, r, d):
                self.X = x
                self.Y = y
                self.turnedRight = False
                self.turnedAround = False
                self.turnedLeft = False
                self.Range = r
                self.Dir = d
                self.lastDir = ''
                "empty memory for robot"
                self.Memory = Map(15,20)
                self.XGoal = 13
                self.YGoal = 18
                self.XStart = 1
                self.YStart = 1
                self.StartNode = Node(self.XStart, self.YStart)
                self.GoalNode = Node(self.XGoal, self.YGoal)
                self.enteredGoal=False
                self.mapStr=''
                self.reposFront = False
                self.reposRight = False
                self.reposLeft = False
                self.resetError = False
                self.isWall = False
                self.threeObs = False
                self.androidMapStr=''
                self.pathCommand = ''
                self.decodedPathCmd = ''
                self.lastCorner = 0
                self.justRF = False
                self.startzone = False
                self.startzonepush = True
                self.run = 0
                self.goalzone = 0
                self.loop = False
                self.VirtualMap = Map(15, 20)
                self.ShortestPath = list()
                self.leftReposCount = 0
                self.rightReposCount = 0
        def turnLeft(self):
                if self.Dir=='U':
                        self.Dir = 'L'
                        self.lastDir = 'U' 
                        turnedLeft = True
                elif self.Dir=='D':
                        self.Dir = 'R'
                        self.lastDir = 'D' 
                        turnedLeft = True
                        
                elif self.Dir== 'R':
                        self.Dir = 'U'
                        self.lastDir = 'R' 
                        turnedLeft = True
                        
                elif self.Dir== 'L':
                        self.Dir = 'D'
                        self.lastDir = 'L' 
                        turnedLeft = True
                        
        def turnRight(self):  
                if self.Dir== 'U':
                        self.Dir = 'R'
                        self.lastDir = 'U'
                        self.turnedRight = True
                        
                elif self.Dir== 'D':
                        self.Dir = 'L'
                        self.lastDir = 'D' 
                        self.turnedRight = True
                        
                elif self.Dir== 'R':
                        self.Dir = 'D'
                        self.lastDir = 'R' 
                        self.turnedRight = True
                        
                elif self.Dir== 'L':
                        self.Dir = 'U'
                        self.lastDir = 'L' 
                        self.turnedRight = True

        def moveForward(self,dis):
                if self.Dir== 'U':
                        self.Y+=dis

                elif self.Dir== 'D':
                        self.Y-=dis
                        
                elif self.Dir== 'R':
                        self.X+=dis
                        
                elif self.Dir== 'L':
                        self.X-=dis
        def turnAround(self):
                if self.Dir == 'U':
                        self.Dir = 'D'
                        self.lastDir = 'U'
                        self.turnedAround = True
                        
                elif self.Dir== 'D':
                        self.Dir = 'U'
                        self.lastDir = 'D' 
                        self.turnedAround = True
                        
                elif self.Dir== 'R':
                        self.Dir = 'L'
                        self.lastDir = 'R'
                        self.turnedAround = True

                elif self.Dir== 'L':
                        self.Dir = 'R'
                        self.lastDir = 'L'
                        self.turnedAround = True
        def inStartZone(self):
                if self.X == 1 and self.Y == 1:
                        return True

        def explore(self,ArStr):
                print "Current X= ", self.X, " Current Y = ", self.Y
                print "Dir = ", self.Dir
                self.reset()
                try:
                        #check front and right before checking left, avoid  conflict
                        isBlockedFront = self.checkTopSide(ArStr)
                        isBlockedRight = self.checkRightSide(ArStr)
                        isBlockedLeft = self.checkLeftSide(ArStr)

                        if ((self.X == 12 or self.X==13 )and (self.Y==17 or self.Y==18)):
                                self.enteredGoal = True

                        checkinStartzone = self.inStartZone()

                        if checkinStartzone == True and self.enteredGoal == True:
                                self.clearGoalZone()
                                self.generateMapStr()
                                self.generateAndroidMapStr()
                                return 'F'
                        #repos front call
                        print 'ReposFront \t\t\t', self.reposFront
                        print 'ReposRight \t\t\t', self.reposRight
                        print 'ReposLeft \t\t\t', self.reposLeft

                        if(self.justRF):
                                self.leftReposCount = 2
                                self.rightReposCount = 2

                        if(self.reposFront):
                                self.justRF = True
                        else:
                                self.justRF = False
                        
                        if(self.reposFront and self.reposRight and self.lastCorner == 0):
                                print 'Reseting error...'
                                self.lastCorner = 1
                                self.generateMapStr()
                                self.generateAndroidMapStr()
                                self.printMemory()
                                return '7'
                        #need to confirm what 7 does
                        if(self.lastCorner == 1):
                                print 'Turn left'
                                self.lastCorner = 0
                                #reset counter at corner
                                self.rightReposCount = 3
                                self.leftReposCount = 3
                                self.turnLeft()
                                self.printMemory()
                                return '3'
                                
                        if(self.reposLeft):
                                self.leftReposCount +=1
                        else:
                                self.leftReposCount = 0
                        
                        
                        if(self.leftReposCount == 4):
                                self.leftReposCount = 0

                        if(self.reposRight):
                                self.rightReposCount +=1
                        else:
                                self.rightReposCount = 0

                        if(self.rightReposCount == 4):
                                self.rightReposCount = 0

                        if(self.reposRight and self.rightReposCount == 1):
                                print 'Repos right'
                                self.leftReposCount = 1
                                return '9'
                        
                        
                        #repos left after every 3 moves
                        if(self.reposLeft and self.leftReposCount == 1):
                                print 'Repos left'
                                return '8'
                        
                        if(self.reposFront and not self.justRF):
                                print "Realigning front, not at corner... "
                                self.justRF = True
                                #in case there are some changes
                                self.generateMapStr();
                                self.generateAndroidMapStr()
                                self.printMemory()
                                return '5'
                        else:
                                self.justRF = False

                        # not using for now
                        if(self.resetError):
                                print "Resetting error, not at corner..."
                                #in case there are some changes
                                self.generateMapStr()
                                self.generateAndroidMapStr()
                                self.printMemory()
                                return '7'

                        if (not isBlockedRight and  not self.turnedRight):
                                print("Turn right")
                                self.turnRight()
                                self.generateMapStr()
                                self.generateAndroidMapStr()
                                self.printMemory()
                                return "2"
                        elif (not isBlockedFront):
                                print("Move Forward")
                                self.moveForward(1)
                                self.generateMapStr()
                                self.generateAndroidMapStr()
                                self.printMemory()
                                self.turnedRight = False
                                return "1"
                        elif (not isBlockedLeft):
                                print("Turn left")
                                self.turnedRight = False
                                self.turnLeft()
                                self.generateMapStr()
                                self.generateAndroidMapStr()
                                self.printMemory()
                                return "3"
                        else:
                                # should turn left here in case it detects wrong obs
                                print("Turn left")
                                self.turnLeft()
                                self.generateMapStr()
                                self.generateAndroidMapStr()
                                self.printMemory()
                                self.turnedRight = False
                                return "3"
                except ValueError as e:
                        print(e.Message)
                        print(e)
                print 
        def reset(self):
                self.isWall = False
                self.threeObs = False
                self.reposFront = False
                self.reposLeft = False
                self.reposRight = False
                self.resetError = False
        
        def checkLeftSide(self, ArStr):
                print "checking left side"

                isBlocked = False
                #this time is for checking wall
                if self.Dir == 'R':
                        isBlocked = self.checkTop()
                if self.Dir == 'U':
                        isBlocked = self.checkLeft()
                if self.Dir == 'L':
                        isBlocked = self.checkBottom()
                if self.Dir == 'D':
                        isBlocked = self.checkRight()

                if(not self.isWall):
                        if(ArStr[0] == '1'):
                                self.updateMap(0, 1)
                                isBlocked = True
                        else:
                                self.updateMap(0, 2)

                #after updating memory
                if self.Dir == 'R':
                        isBlocked = self.checkTop()
                if self.Dir == 'U':
                        isBlocked = self.checkLeft()
                if self.Dir == 'L':
                        isBlocked = self.checkBottom()
                if self.Dir == 'D':
                        isBlocked = self.checkRight()

                if(self.isWall or self.threeObs):
                        self.reposLeft = True
                        isBlocked = True
                self.isWall = False
                self.threeObs = False
                print "LEFT \t\t\t", isBlocked
                if(isBlocked):
                        return True
                return isBlocked
        
        def checkTopSide(self, ArStr):
                print "checking top side"
                isBlocked = False

                #checking wall
                if self.Dir == 'R':
                        isBlocked = self.checkRight()
                if self.Dir == 'U':
                        isBlocked = self.checkTop()
                if self.Dir == 'L':
                        isBlocked = self.checkLeft()
                if self.Dir == 'D':
                        isBlocked = self.checkBottom()
                
                if(not self.isWall):
                        for i in range(1,4):
                                if (ArStr[i]=='1'):
                                        self.updateMap(i, 1)
                                        isBlocked = True
                                else:
                                        self.updateMap(i, 2)
                #check again after updating memory
                if self.Dir == 'R':
                        isBlocked = self.checkRight()
                if self.Dir == 'U':
                        isBlocked = self.checkTop()
                if self.Dir == 'L':
                        isBlocked = self.checkLeft()
                if self.Dir == 'D':
                        isBlocked = self.checkBottom()

                if (self.isWall or self.threeObs):
                        print 'setting repost front true'
                        self.reposFront = True
                        isBlocked = True

                self.isWall = False
                self.threeObs = False        
                print "TOP \t\t\t", isBlocked
                return isBlocked

        def checkRightSide(self, ArStr):
                print "checking right side"
                isBlocked = False
                if self.Dir == 'R':
                        isBlocked = self.checkBottom()
                if self.Dir == 'U':
                        isBlocked = self.checkRight()
                if self.Dir == 'L':
                        isBlocked = self.checkTop()
                if self.Dir == 'D':
                        isBlocked = self.checkLeft()

                if self.threeObs:
                        self.threeObs = False
                        self.isWall = False
                        self.reposRight = True
                        return True
                #update memory
                if(not self.isWall):
                        if(ArStr[4] == '1'):
                                self.updateMap(4, 1)
                        else:
                                self.updateMap(4, 2)
                        if(ArStr[6] == '1'):
                                self.updateMap(6, 1)
                        else:
                                self.updateMap(6, 2)
                #after updating memory
                if self.Dir == 'R':
                        isBlocked = self.checkBottom()
                if self.Dir == 'U':
                        isBlocked = self.checkRight()
                if self.Dir == 'L':
                        isBlocked = self.checkTop()
                if self.Dir == 'D':
                        isBlocked = self.checkLeft()

                if(self.isWall or self.threeObs):
                        self.reposRight = True
                self.isWall = False
                self.threeObs = False

                print "RIGHT \t\t\t", isBlocked
                return isBlocked

        def updateMap(self, pos, val):
                if(self.Dir == 'U'):
                        if(pos == 0):
                                self.Memory.grid[self.Y + 1][self.X -2] = val
                        if(pos == 1):
                                self.Memory.grid[self.Y + 2][self.X - 1] = val
                        if(pos == 2):
                                self.Memory.grid[self.Y + 2][self.X] = val
                        if(pos == 3):
                                self.Memory.grid[self.Y + 2][self.X + 1] = val
                        if(pos == 4):
                                #dont update if there is an obs on the right in mem, prevent loop
                                if(self.Memory.grid[self.Y + 1][self.X + 2] == 1):
                                        return
                                self.Memory.grid[self.Y + 1][self.X + 2] = val
                        if(pos == 5):
                                self.Memory.grid[self.Y][self.X + 2] = val
                        if(pos == 6):
                                #dont update if there is an obs on the right in mem, prevent loop
                                if(self.Memory.grid[self.Y-1][self.X + 2] == 1):
                                        return
                                self.Memory.grid[self.Y-1][self.X + 2] = val
                elif(self.Dir == 'R'):
                        if(pos == 0):
                                self.Memory.grid[self.Y+2][self.X + 1] = val
                        if(pos == 1):
                                self.Memory.grid[self.Y+1][self.X + 2] = val
                        if(pos == 2):
                                self.Memory.grid[self.Y][self.X+2] = val
                        if(pos == 3):
                                self.Memory.grid[self.Y-1][self.X +2] = val
                        if(pos == 4):
                                if(self.Memory.grid[self.Y-2][self.X+1] == 1):
                                        return
                                self.Memory.grid[self.Y-2][self.X+1] = val
                        if(pos == 5):
                                self.Memory.grid[self.Y-2][self.X] = val
                        if(pos == 6):
                                if(self.Memory.grid[self.Y-2][self.X-1] == 1):
                                        return
                                self.Memory.grid[self.Y-2][self.X-1] = val
                elif(self.Dir == 'D'):
                        if(pos == 0):
                                self.Memory.grid[self.Y-1][self.X +2] = val
                        if(pos == 1):
                                self.Memory.grid[self.Y-2][self.X+1] = val
                        if(pos == 2):
                                self.Memory.grid[self.Y-2][self.X] = val
                        if(pos == 3):
                                self.Memory.grid[self.Y-2][self.X-1] = val
                        if(pos == 4):
                                if(self.Memory.grid[self.Y-1][self.X- 2] == 1):
                                        return
                                self.Memory.grid[self.Y-1][self.X- 2] = val
                        if(pos == 5):
                                self.Memory.grid[self.Y][self.X-2] = val
                        if(pos == 6):
                                if(self.Memory.grid[self.Y+1][self.X -2] == 1):
                                        return
                                self.Memory.grid[self.Y+1][self.X -2] = val
                elif(self.Dir == 'L'):
                        if(pos == 0):
                                self.Memory.grid[self.Y-2][self.X - 1] = val
                        if(pos == 1):
                                self.Memory.grid[self.Y-1][self.X - 2] = val
                        if(pos == 2):
                                self.Memory.grid[self.Y][self.X-2] = val
                        if(pos == 3):
                                self.Memory.grid[self.Y+1][self.X - 2] = val
                        if(pos == 4):
                                if(self.Memory.grid[self.Y+2][self.X - 1] == 1):
                                        return
                                self.Memory.grid[self.Y+2][self.X - 1] = val
                        if(pos == 5):
                                self.Memory.grid[self.Y+2][self.X] = val
                        if(pos == 6):
                                if(self.Memory.grid[self.Y+2][self.X + 1] == 1):
                                        return
                                self.Memory.grid[self.Y+2][self.X + 1] = val

        def checkTop(self):
                temp1 = False
                temp2 = False
                temp3 = False
                isBlocked = False
                # wall
                if(self.Y + self.Range + 1 >= self.Memory.height):
                        self.threeObs = True
                        self.isWall = True
                        return True
                if(self.Memory.grid[self.Y + 2][self.X -1] == 1):
                        isBlocked = True
                        temp1 = True
                
                if(self.Memory.grid[self.Y + 2][self.X] == 1):
                        isBlocked = True
                        temp2 = True
                
                if(self.Memory.grid[self.Y + 2][self.X + 1]== 1):
                        isBlocked = True
                        temp3 = True

                #3 obstacles on top side
                if(temp1 and temp2 and temp3):
                        self.threeObs = True
                else:
                        self.threeObs = False
                return isBlocked

        def checkLeft(self):
                temp1 = False
                temp2 = False
                temp3 = False
                isBlocked = False
                # wall
                if(self.X - self.Range - 1 < 0):
                        self.isWall = True
                        self.threeObs = True
                        return True
                
                if(self.Memory.grid[self.Y + 1][self.X - 2] == 1):
                        isBlocked = True
                        temp1 = True
                
                if(self.Memory.grid[self.Y][self.X - 2] == 1):
                        isBlocked = True
                        temp2 = True
                
                if(self.Memory.grid[self.Y -1 ][self.X - 2]== 1):
                        isBlocked = True
                        temp3 = True

                if(temp1 and temp2 and temp3):
                        self.threeObs = True
                else:
                        self.threeObs = False
                return isBlocked
        def checkRight(self):
                isBlocked = False
                temp1 = False
                temp2 = False
                temp3 = False
                if(self.X + self.Range + 1 >= self.Memory.width):
                        self.isWall = True
                        self.threeObs = True
                        return True
                if(self.Memory.grid[self.Y + 1][self.X + 2] == 1):
                        isBlocked = True
                        temp1 = True
                if(self.Memory.grid[self.Y][self.X+2] == 1):
                        isBlocked = True
                        temp2 = True
                if(self.Memory.grid[self.Y -1][self.X + 2] == 1):
                        isBlocked = True
                        temp3 = True
                if(temp1 and temp2 and temp3):
                        self.threeObs = True
                else:
                        self.threeObs = False
                return isBlocked
        def checkBottom(self):
                temp1 = False
                temp2 = False
                temp3 = False
                isBlocked = False
                if(self.Y - self.Range - 1 < 0):
                        self.isWall = True
                        self.threeObs = True
                        return True

                if(self.Memory.grid[self.Y-2][self.X - 1] == 1):
                        isBlocked = True
                        temp1 = True
                if(self.Memory.grid[self.Y - 2][self.X] == 1):
                        isBlocked = True
                        temp2 = True
                if(self.Memory.grid[self.Y - 2][self.X + 1]== 1):
                        isBlocked = True
                        temp3 = True
                if(temp1 and temp2 and temp3):
                        self.threeObs = True
                else:
                        self.threeObs = False
                return isBlocked

        def generateMapStr(self):
                # first 5 characters: direction + current center position
                if (self.X < 10):
                        x = '0'+ str(self.X)
                else:
                        x = str(self.X)
                if (self.Y < 10):
                        y = '0'+ str(self.Y)
                else:
                        y = str(self.Y) 
                self.mapStr = self.Dir + x + y
                
                # iterate the map to add value to mapStr
                if (self.inStartZone() and self.enteredGoal):
                        # self.clearGoalZone()
                        for i in range (20):
                                for j in range (15):
                                        self.mapStr += str(self.Memory.grid[i][j])
                        self.mapStr += 'F'
                else:
                        for i in range (20):
                                for j in range (15):
                                        self.mapStr += str(self.Memory.grid[i][j])
         
        def clearGoalZone(self):
                if (self.Memory.grid[17][11]==1 or self.Memory.grid[18][11]==1 or self.Memory.grid[19][11]==1) and (self.Memory.grid[16][12]==1 or self.Memory.grid[16][13]==1 or self.Memory.grid[16][14]==1):
                        self.Memory.grid[16][12] = 2
                        self.Memory.grid[16][13] = 2
                        self.Memory.grid[16][14] = 2
                if self.Memory.grid[16][11]==1 and (self.Memory.grid[17][11]==1 or self.Memory.grid[18][11]==1 or self.Memory.grid[19][11]==1) and (self.Memory.grid[16][12]==1 or self.Memory.grid[16][13]==1 or self.Memory.grid[16][14]==1):
                        self.Memory.grid[16][12] = 2
                        self.Memory.grid[16][13] = 2
                        self.Memory.grid[16][14] = 2
                if (self.Memory.grid[17][14]==1) and (self.Memory.grid[16][14]==1):
                        self.Memory.grid[16][14] = 2
                for i in range (17, 20):
                                for j in range (12, 15):
                                        self.Memory.grid[i][j] = 2
                for i in range (0, 4):
                                for j in range (0, 4):
                                        self.Memory.grid[i][j] = 2
                
        def generateAndroidMapStr(self):
                # first 9 characters: GRID + direction + current center position
                if (self.X < 9):
                        x = '0'+ str(self.X+1)
                else:
                        x = str(self.X+1)
                if (self.Y < 9):
                        y = '0'+ str(self.Y+1)
                else:
                        y = str(self.Y+1) 
                self.androidMapStr = 'GRID' + self.Dir + y + x
                
                # iterate the map to add value to androidMapStr
                if (self.inStartZone() and self.enteredGoal):
                        #self.clearGoalZone()
                        for i in range (15):
                                for j in range (20):
                                        self.androidMapStr += str(self.Memory.grid[j][i])
                        self.androidMapStr += 'F'
                else:
                        for i in range (15):
                                for j in range (20):
                                        self.androidMapStr += str(self.Memory.grid[j][i])
                        self.androidMapStr += 'P'
        
        def startZoneRealign(self):
                if(self.Dir == 'D' and self.startzonepush):
                        self.startzonepush = False
                        return '7'
                if self.Dir == 'D':
                        self.turnRight()
                        self.generateMapStr()
                        self.generateAndroidMapStr()
                        return '2'
                elif (not self.startzone and not self.Dir == 'R' and not self.Dir == 'U'):
                        self.startzone = True
                        return '5'
                elif self.Dir == 'L':
                        self.turnRight()
                        self.generateMapStr()
                        self.generateAndroidMapStr()
                        return '2'
                elif self.Dir == 'R':
                        self.turnLeft()
                        self.generateMapStr()
                        self.generateAndroidMapStr()
                        return '3'
                else:
                        return
                
        # one by one grid      
        '''
        def fastestPathDecoder(self, pcStr):
                pcStr = pcStr[1:len(pcStr)]
                for i in range (len(pcStr)):
                        if pcStr[i] == 'M':
                                self.pathCommand += '1'
                        elif pcStr[i] == 'R':
                                self.pathCommand += '2'
                        elif pcStr[i] == 'L':
                                self.pathCommand += '3'
                        else:
                                return
        '''
        #multiple grids
        def fastestPathDecoder(self):
                i = 0
                while (i<len(self.pathCommand)):
                        if self.pathCommand[i] == 'M':
                                countM = 0
                                while(self.pathCommand[i] == 'M'):
                                        countM += 1
                                        if (i+1< len(self.pathCommand)):
                                                i += 1
                                        else:
                                                break
                                for j in range (countM / 3):
                                        self.decodedPathCmd += 'b'
                                if (countM%3==1):
                                        self.decodedPathCmd += '1'
                                elif (countM%3==2):
                                        self.decodedPathCmd += 'a'
                                '''
                                elif (countM%5==3):
                                        self.pathCommand += 'b'
                                elif (countM%5==4):
                                        self.pathCommand += 'c'
                                '''
                        if self.pathCommand[i] == 'R':
                                self.decodedPathCmd += '2'
                        if self.pathCommand[i] == 'L':
                                self.decodedPathCmd += '3'
                        i += 1
                print self.decodedPathCmd
        def checkBeforeTurn(self, arStr):
                if(self.decodedPathCmd[self.run - 1] == '2'):
                        #ok to move
                        if(arStr[1] == '0' and arStr[2] == '0' and arStr[3] == '0'):
                                return 0
                        #short a bit <= 1 grid ()
                        if(arStr[1] == '0' and arStr[2] == '0' and arStr[3] == '1'):
                                return 0
                        #short x grids (1<x<=2) or exceed 3 grids (less likely)
                        if(arStr[1] == '0' and arStr[2] == '1' and arStr[3] == '1'):
                                return 0
                        #need to check with memory to determine where robot is currently is
                        if(arStr[1] == '1' and arStr[2] == '1' and arStr[3] == '1'):
                                return 0
                        #exceed 1 grid
                        if(arStr[1] == '1' and arStr[2] == '0' and arStr[3] == '0'):
                                return 0
                        #check with memory, short 2 or exceed 2, rarely happen
                        if(arStr[1] == '0' and arStr[2] == '1' and arStr[3] == '0'):
                                return 0
                        #short 3 or exceed 2, very rare
                        if(arStr[1] == '1' and arStr[2] == '1' and arStr[3] == '0'):
                                return 0
                        #short 3 or exceed 3, fucking rare
                        if(arStr[1] == '1' and arStr[2] == '0' and arStr[3] == '1'):
                                return 0
                if(self.decodedPathCmd[self.run - 1] == '3'):
                        #ok to move
                        if(arStr[1] == '0' and arStr[2] == '0' and arStr[3] == '0'):
                                return 0
                        #exceed 1 grid or less
                        if(arStr[1] == '0' and arStr[2] == '0' and arStr[3] == '1'):
                                return 0
                        #exceed 2 or short 3
                        if(arStr[1] == '0' and arStr[2] == '1' and arStr[3] == '1'):
                                return 0
                        # need to check with memory to determine where robot is currently is
                        if(arStr[1] == '1' and arStr[2] == '1' and arStr[3] == '1'):
                                return 0
                        #short 1
                        if(arStr[1] == '1' and arStr[2] == '0' and arStr[3] == '0'):
                                return 0
                        #check with memory, short 2 or exceed 2, rarely happen
                        if(arStr[1] == '0' and arStr[2] == '1' and arStr[3] == '0'):
                                return 0
                        #short 2 or exceed 3, very rare
                        if(arStr[1] == '1' and arStr[2] == '1' and arStr[3] == '0'):
                                return 0
                        #short 3 or exceed 3, fucking rare
                        if(arStr[1] == '1' and arStr[2] == '0' and arStr[3] == '1'):
                                return 0
        def getExpectedReadings(self):
                expected = ""
                if(self.Dir == 'U'):
                        #0
                        if(self.Memory.grid[self.Y+1][self.X-2] == 1):
                                expected +='1'
                        else:
                                expected +='0'
                        #1
                        if(self.Memory.grid[self.Y+2][self.X-1] == 1):
                                expected +='1'
                        else:
                                expected +='0'
                        #2
                        if(self.Memory.grid[self.Y+2][self.X] == 1):
                                expected +='1'
                        else:
                                expected +='0'
                        #3
                        if(self.Memory.grid[self.Y+2][self.X+1] == 1):
                                expected +='1'
                        else:
                                expected +='0'
                        #4
                        if(self.Memory.grid[self.Y+1][self.X+2] == 1):
                                expected +='1'
                        else:
                                expected +='0'
                        #5
                        expected += '0'
                        #6
                        if(self.Memory.grid[self.Y-1][self.X+2] == 1):
                                expected +='1'
                        else:
                                expected +='0'
                if(self.Dir == 'R'):
                        #0
                        if(self.Memory.grid[self.Y+2][self.X+1] == 1):
                                expected +='1'
                        else:
                                expected +='0'
                        #1
                        if(self.Memory.grid[self.Y+1][self.X+2] == 1):
                                expected +='1'
                        else:
                                expected +='0'
                        #2
                        if(self.Memory.grid[self.Y][self.X+2] == 1):
                                expected +='1'
                        else:
                                expected +='0'
                        #3
                        if(self.Memory.grid[self.Y-1][self.X+2] == 1):
                                expected +='1'
                        else:
                                expected +='0'
                        #4
                        if(self.Memory.grid[self.Y-2][self.X+1] == 1):
                                expected +='1'
                        else:
                                expected +='0'
                        #5
                        expected += '0'
                        #6
                        if(self.Memory.grid[self.Y-2][self.X-1] == 1):
                                expected +='1'
                        else:
                                expected +='0'

                if(self.Dir == 'L'):
                        #0
                        if(self.Memory.grid[self.Y-2][self.X-1] == 1):
                                expected +='1'
                        else:
                                expected +='0'
                        #1
                        if(self.Memory.grid[self.Y-1][self.X-2] == 1):
                                expected +='1'
                        else:
                                expected +='0'
                        #2
                        if(self.Memory.grid[self.Y][self.X-2] == 1):
                                expected +='1'
                        else:
                                expected +='0'
                        #3
                        if(self.Memory.grid[self.Y+1][self.X-2] == 1):
                                expected +='1'
                        else:
                                expected +='0'
                        #4
                        if(self.Memory.grid[self.Y+2][self.X-1] == 1):
                                expected +='1'
                        else:
                                expected +='0'
                        #5
                        expected += '0'
                        #6
                        if(self.Memory.grid[self.Y+2][self.X+1] == 1):
                                expected +='1'
                        else:
                                expected +='0'
                if(self.Dir == 'D'):
                        #0
                        if(self.Memory.grid[self.Y-1][self.X+2] == 1):
                                expected +='1'
                        else:
                                expected +='0'
                        #1
                        if(self.Memory.grid[self.Y-2][self.X+1] == 1):
                                expected +='1'
                        else:
                                expected +='0'
                        #2
                        if(self.Memory.grid[self.Y-2][self.X] == 1):
                                expected +='1'
                        else:
                                expected +='0'
                        #3
                        if(self.Memory.grid[self.Y-2][self.X-1] == 1):
                                expected +='1'
                        else:
                                expected +='0'
                        #4
                        if(self.Memory.grid[self.Y-1][self.X-2] == 1):
                                expected +='1'
                        else:
                                expected +='0'
                        #5
                        expected += '0'
                        #6
                        if(self.Memory.grid[self.Y+1][self.X-2] == 1):
                                expected +='1'
                        else:
                                expected +='0'
                return expected
        def checkSensorReadings(self, arStr):
                expected = getExpectedReadings()
                #about to move forward
                #if(self.decodedPathCmd[self.run + 1] == '1'):
                        
        def fastestRun(self,arStr):
                temp = 1
                if(self.Y == 18 and self.X == 13):
                        return 'F'
                #if(arStr[2] == '1'):
                if (self.run < len(self.decodedPathCmd)):
                        if (self.decodedPathCmd[self.run] == '1'):
                                self.moveForward(1)
                        elif (self.decodedPathCmd[self.run] == '2'):
                                self.turnRight()
                        elif (self.decodedPathCmd[self.run] == '3'):
                                self.turnLeft()
                        elif (self.decodedPathCmd [self.run] == 'a'):
                                self.moveForward(2)
                        elif (self.decodedPathCmd[self.run] == 'b'):
                                self.moveForward(3)
                        elif (self.decodedPathCmd[self.run] == 'c'):
                                self.moveForward(4)
                        elif (self.decodedPathCmd[self.run] == 'd'):
                                self.moveForward(5)
                        temp = self.decodedPathCmd[self.run]
                        self.run += 1
                
                self.generateMapStr()
                self.generateAndroidMapStr() 
                print "currrent position: X = ", self.X, "Y = ", self.Y, "Direction: ", self.Dir
                return temp

        def printMemory(self):
                return
                for i in range(20):
                        for j in range (15):
                                if(self.X == j and self.Y == 19-i):
                                        print 'X', ' ',
                                else:
                                        print self.Memory.grid[19-i][j], ' ',
                        print 


        def goalzoneRealign(self):
                if(self.goalzone == 6 or self.goalzone == 3):
                        return 'C'
                if self.Dir == 'U' and self.goalzone != 1 and self.goalzone != 5:
                        self.goalzone = 1
                        return '6'

                if self.goalzone == 1:
                        self.goalzone = 2
                        self.turnRight()
                        return '2'

                if self.goalzone == 2:
                        self.goalzone = 3
                        return '6'

                if self.Dir == 'R' and self.goalzone != 4:
                        self.goalzone = 4
                        return '6'
                if self.goalzone == 4:
                        self.goalzone = 5
                        self.turnLeft()
                        return '3'

                if self.goalzone == 5:
                        self.goalzone = 6
                        return '6'
                
        def fastestPathCompute(self):
                self.printMemory()
                closedSet = list()
                openSet = list()
                neighbors = list()
                currentNode = Node(0, 0)
                self.StartNode.GCost = 0
                self.StartNode.FCost = self.StartNode.GCost + self.computeH(self.StartNode)
                openSet.append(self.StartNode)
                self.Dir = 'U'
                for y in range(20):
                        for x in range(15):
                                if(self.Memory.grid[y][x] == 0):
                                        self.Memory.grid[y][x] = 1
                self.processVirtualMap()
                while(len(openSet) != 0):
                        self.sortOpenSet(openSet)
                        currentNode = openSet.pop(0)
                        if(currentNode.XNode == self.GoalNode.XNode and currentNode.YNode == self.GoalNode.YNode):
                                self.constructFastestPath(currentNode)
                                break
                        closedSet.append(currentNode)
                        neighbors = self.getNeighbors(currentNode, openSet)
                        lastNode = currentNode.CameFrom
                        for neighbor in neighbors:
                                if(self.checkNodeInSet(neighbor, closedSet)):
                                        continue
                                tentativeGCost = currentNode.GCost + 1 + self.turningCost(lastNode, neighbor)
                                inOpenSet = self.checkNodeInSet(neighbor, openSet)
                                if(not inOpenSet or tentativeGCost < neighbor.GCost):
                                        neighbor.CameFrom = currentNode
                                        neighbor.GCost = tentativeGCost
                                        neighbor.FCost = neighbor.GCost + neighbor.HCost
                                        if(not inOpenSet):
                                                openSet.append(neighbor)

                print 'out of while loop'
                self.fastestPathDecoder()
                self.X = 1
                self.Y = 1
                self.Dir = 'U'

        def computeH(self, node):
                return (self.XGoal - node.XNode) + (self.YGoal - node.YNode)

        #Sort open set, lowest fcost on top
        def sortOpenSet(self, openSet):
                for i in range(len(openSet)):
                        if openSet[i].FCost < openSet[0].FCost:
                                openSet[i], openSet [0] = openSet[0], openSet[i]
        def processVirtualMap(self):
                for i in range(20):
                        for j in range(15):
                                if(i == 0 or j == 0 or i == 19 or j == 14):
                                        self.VirtualMap.grid[i][j] = 1
                                if(self.Memory.grid[i][j] == 1):
                                        for m in range(i-1, i+2):
                                                for n in range(j-1, j+2):
                                                        if(m<0 or n<0 or m>19 or n>14):
                                                                continue
                                                        try:
                                                                self.VirtualMap.grid[m][n] = 1
                                                        except Exception, e:
                                                                print 'failed in generating virtual map'
                                if(self.VirtualMap.grid[i][j] == 0):
                                        self.VirtualMap.grid[i][j] = self.Memory.grid[i][j]                            

        def getNeighbors(self, currentNode, openSet):
                x = currentNode.XNode
                y = currentNode.YNode
                neighbors = list()
                if(self.VirtualMap.grid[y][x+1] == 2):
                        neighbor = Node(x+1, y)
                        neighbor.HCost = self.computeH(neighbor)
                        temp = self.getNodeInSet(neighbor, openSet)
                        if temp is None:
                                neighbors.append(neighbor)
                        else:
                                neighbors.append(temp)
                if(self.VirtualMap.grid[y][x-1] == 2):
                        neighbor = Node(x-1, y)
                        neighbor.HCost = self.computeH(neighbor)
                        temp = self.getNodeInSet(neighbor, openSet)
                        if temp is None:
                                neighbors.append(neighbor)
                        else:
                                neighbors.append(temp)
                if(self.VirtualMap.grid[y-1][x] == 2):
                        neighbor = Node(x, y-1)
                        neighbor.HCost = self.computeH(neighbor)
                        temp = self.getNodeInSet(neighbor, openSet)
                        if temp is None:
                                neighbors.append(neighbor)
                        else:
                                neighbors.append(temp)
                if(self.VirtualMap.grid[y+1][x] == 2):
                        neighbor = Node(x, y+1)
                        neighbor.HCost = self.computeH(neighbor)
                        temp = self.getNodeInSet(neighbor, openSet)
                        if temp is None:
                                neighbors.append(neighbor)
                        else:
                                neighbors.append(temp)
                return neighbors
        def checkNodeInSet(self, node, listNodes):
                for item in listNodes:
                        if (node.XNode == item.XNode and node.YNode == item.YNode):
                                return True
                return False

        def turningCost(self, lastNode, nextNode):
                if(lastNode == None):
                        return 0
                if(lastNode.XNode != nextNode.XNode and lastNode.YNode != nextNode.YNode):
                        return 10
                return 0
        def constructFastestPath(self, node):
                self.ShortestPath.append(node)
                self.X = 1
                self.Y =1
                self.Dir = 'U'
                temp = node.CameFrom
                print 'constructing path'
                while(not (temp.XNode == self.StartNode.XNode and temp.YNode == self.StartNode.YNode) and not temp == None):
                        self.ShortestPath.append(temp)
                        temp = temp.CameFrom

                self.ShortestPath = self.ShortestPath[::-1]
                currentNode = self.ShortestPath[0]
                for item in self.ShortestPath:
                        if(self.Dir == 'U'):
                                if(item.XNode > self.X):
                                        self.turnRight()
                                        self.moveForward(1)
                                        self.pathCommand += 'R'
                                elif item.YNode > self.Y:
                                        self.moveForward(1)
                                elif item.XNode < self.X:
                                        self.turnLeft()
                                        self.moveForward(1)
                                        self.pathCommand+='L'
                        elif self.Dir == 'R':
                                if(item.XNode > self.X):
                                        self.moveForward(1)
                                elif item.YNode > self.Y:
                                        self.turnLeft()
                                        self.moveForward(1)
                                        self.pathCommand+='L'
                                elif item.YNode < self.Y:
                                        self.turnRight()
                                        self.moveForward(1)
                                        self.pathCommand+='R'
                        elif self.Dir == 'D':
                                if(item.XNode > self.X):
                                        self.turnLeft()
                                        self.moveForward(1)
                                        self.pathCommand+='L'
                                elif item.YNode < self.Y:
                                        self.moveForward(1)
                                elif item.XNode < self.X:
                                        self.turnRight()
                                        self.moveForward(1)
                                        self.pathCommand+='R'
                        elif self.Dir == 'L':
                                if(item.XNode < self.X):
                                        self.moveForward(1)
                                elif item.YNode > self.Y:
                                        self.turnRight()
                                        self.moveForward(1)
                                        self.pathCommand+='R'
                                elif item.YNode < self.Y:
                                        self.turnLeft()
                                        self.moveForward(1)
                                        self.pathCommand+='L'
                        self.pathCommand += 'M'
                self.printVirtualMap()
                print self.pathCommand
                print len(self.pathCommand)

        def getNodeInSet(self, node, listNodes):
                for item in listNodes:
                        if(item.XNode == node.XNode and item.YNode == node.YNode):
                                return item
                return None
        def printVirtualMap(self):
                for x in range(20):
                        for y in range(15):
                                print self.VirtualMap.grid[19-x][y], ' ',
                        print 
