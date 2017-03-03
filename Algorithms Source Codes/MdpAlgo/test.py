
def convert (msg):
    new_list = ['l','l']
    #cur_dir = self.map.get_robot_direction()
    cur_dir = 'S'
    if ((msg[0] == 'N') and(cur_dir == 'S')):
        new_list = ['l','l','f']
    elif ((msg[0] == 'N') and(cur_dir == 'W')):
        new_list = ['r','f']
    elif ((msg[0] == 'E') and(cur_dir == 'S')):
        new_list = ['l','f']
    elif ((msg[0] == 'E') and(cur_dir == 'W')):
        new_list = ['l','l','f']    
    for i in range (1,len(msg)):
        if (msg[i] == msg[i-1]):
            new_list.append('f')
        elif (\
            (msg[i-1]== 'N' and msg[i] == 'S') or\
            (msg[i-1]== 'E' and msg[i] == 'W') or\
            (msg[i-1]== 'S' and msg[i] == 'N') or\
            (msg[i-1]== 'W' and msg[i] == 'E')):
            new_list.append ('l')
            new_list.append ('l')
            new_list.append ('f')
        elif (\
            (msg[i-1]== 'N' and msg[i] == 'E') or\
            (msg[i-1]== 'E' and msg[i] == 'S') or\
            (msg[i-1]== 'S' and msg[i] == 'W') or\
            (msg[i-1]== 'W' and msg[i] == 'N')):
            new_list.append ('r')
            new_list.append ('f')
        elif (\
            (msg[i-1]== 'N' and msg[i] == 'W') or\
            (msg[i-1]== 'E' and msg[i] == 'N') or\
            (msg[i-1]== 'S' and msg[i] == 'E') or\
            (msg[i-1]== 'W' and msg[i] == 'S')):
            new_list.append ('l')
            new_list.append ('f')

    return new_list
print("['N','S','S','E','W','N']")
print (convert(['N','S','S','E','W','N']))
