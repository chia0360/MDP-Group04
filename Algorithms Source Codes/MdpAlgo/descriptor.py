
# ------------------------------------------------------------------------------------------
# Generate map descriptor
# descriptor1: Mark each unexplored square as 0 and each explored square as 1
# descriptor2: Only grid cells marked as “explored” in Part 1 are represented here by a bit.
# Mark cells known to be empty space with 0, mark cells known to contain an obstacle with 1
# -------------------------------------------------------------------------------------------
import config
import mapclass
class descriptor:
    def __init__(self):
        self.map = mapclass.Map().get_map()
        # print(self.map)

    def descriptor1(self):
        # print(self.map)
        rotated = list(zip(*(self.map)))[::-1]
        # print(rotated)
        ret = "11" #padded
        
        for i in range (19,-1,-1):
            for j in range(15):
                if (rotated[i][j] == 0):
                    ret+="0"
                elif (rotated[i][j] == 1):
                    ret += "1"
                elif (rotated[i][j] == 2):
                    ret += "1"
            
        ret += "11" #padded
        hexa = ""
        for i in range(0,len(ret),4):
            temp = ""
            temp += ret[i:i+1]
            temp += ret[i+1:i+2]
            temp += ret[i+2:i+3]
            temp += ret[i+3:i+4]
            hexa += str(hex(int(temp,2)))[2:3]
        return (hexa)
                
    def descriptor2(self):
        # print(self.map)
        rotated = list(zip(*(self.map)))[::-1]
        # print(rotated)
        ret = ""
        cnt = 0
        for i in range (19,-1,-1):
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
        # print(ret)
            
        hexa = ""
        for i in range(0,len(ret),4):
            temp = ""
            temp += ret[i:i+1]
            temp += ret[i+1:i+2]
            temp += ret[i+2:i+3]
            temp += ret[i+3:i+4]
            hexa += str(hex(int(temp,2)))[2:3]
        return(hexa)
# ------------------------------End of class----------------------------------------

