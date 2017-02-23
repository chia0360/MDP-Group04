class temp:
        def __init__(self):
                self.pathCommand = "MMMMMMMMMMMMMMMMMRMMMMMMMMMMMMMMMLMMMMMMMMMMMM"
                self.decodedPathCmd =''

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
                                        for j in range (countM / 10):
                                                self.decodedPathCmd += 'i'
                                        if (countM%10==1):
                                                self.decodedPathCmd += '1'
                                        elif (countM%10==2):
                                                self.decodedPathCmd += 'a'
                                        elif (countM%10==3):
                                                self.decodedPathCmd += 'b'
                                        elif (countM%10==4):
                                                self.decodedPathCmd += 'c'
                                        elif (countM%10==5):
                                                self.decodedPathCmd += 'd'
                                        elif (countM%10==6):
                                                self.decodedPathCmd += 'e'
                                        elif (countM%10==7):
                                                self.decodedPathCmd += 'f'
                                        elif (countM%10==8):
                                                self.decodedPathCmd += 'g'
                                        elif (countM%10==9):
                                                self.decodedPathCmd += 'h'

                                if self.pathCommand[i] == 'R':
                                        self.decodedPathCmd += '2'
                                if self.pathCommand[i] == 'L':
                                        self.decodedPathCmd += '3'
                                i += 1
                        print self.decodedPathCmd

'''
2 grids: a
3 grids: b
4 grids: c
5 grids: d
6 grids: e
7 grids: f
8 grids: g
9 grids: h
10 grids: i
'''