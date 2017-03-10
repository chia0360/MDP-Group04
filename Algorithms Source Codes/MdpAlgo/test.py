def convert (msg):
    new_list = []
    #cur_dir = self.map.get_robot_direction()
    msg = ['S'] + msg[:]

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
    shorten_list = []
    counter = 0
    for item in new_list:
        if item != 'f' and counter != 0:
            if counter >= 10:
                counter1 = counter//2
                counter2 = counter - counter1
                shorten_list.append(counter1)
                shorten_list.append(counter2)
            else:
                shorten_list.append(counter)
            shorten_list.append(item)
            counter = 0
        elif item == 'f':
            counter += 1
    if counter > 0:
        if counter >= 10:
            counter1 = counter//2
            counter2 = counter - counter1
            shorten_list.append(counter1)
            shorten_list.append(counter2)
        else:
            shorten_list.append(counter)

    return shorten_list


print(convert(['S','S','S','S','S','S','S','S','S','S','S','E','E','S','E','E','N','E','E','N','E','E']))

