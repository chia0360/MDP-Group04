#For python simulator
from tkinter import *
from tkinter import ttk
from tkinter import font 

from copy import deepcopy
from logger import *
import time
import handler

class Simulator:
    def __init__(self, title="Arena Simulator"):

        #Instantiate other classes required for simulator
        self.handler = handler.Handler(self)
        self.algo    = self.handler.algo
        self.map     = self.handler.map
        
        #-----------------------------------------------------------------------
        #Simulator
        #-----------------------------------------------------------------------
        self.master  = Tk()
        self.master.title(title)
        t = Toplevel(self.master)

        # Simulator Config Styles
        t.title("Control Panel")
        t.geometry('450x600+1050+28')
        widgetFont = font.Font(family='Times', size=12, weight='bold')
        ttk.Style().configure("TButton", font= widgetFont, padding = 6, relief = "flat", background = "#ccc")
        ttk.Style().configure("TLabel", font=widgetFont)

        # Simulator Control Panel
        self.control_pane = ttk.Frame(t, padding=(24, 20))
        self.control_pane.grid(column=1, row=0, sticky=(N, S, E, W))
        
        # Simulator Map
        self.map_pane = ttk.Frame(self.master, borderwidth=0, relief="solid")
        self.map_pane.grid(column=0, row=0, sticky=(N, S, E, W))
        self.map_widget     = [[None]*self.map.length]*self.map.width

        #-----------------------------------------------------------------------
        # Utilizing pictures for the grid visuals
        #-----------------------------------------------------------------------
    
        # Pictures for the map & legend
        self.map_load_start                 = PhotoImage(file=config.icon_path['start'])
        self.map_start                      = self.map_load_start.subsample(config.icon_path['size'])

        self.map_load_goal                  = PhotoImage(file=config.icon_path['end'])
        self.map_goal                       = self.map_load_goal.subsample(config.icon_path['size'])
        
        self.map_load_free                  = PhotoImage(file=config.icon_path['free'])
        self.map_free                       = self.map_load_free.subsample(config.icon_path['size'])

        self.map_load_free_explored         = PhotoImage(file=config.icon_path['explored_free'])
        self.map_free_explored              = self.map_load_free_explored.subsample(config.icon_path['size'])

        self.map_load_obstacle              = PhotoImage(file=config.icon_path['obstacle'])
        self.map_obstacle                   = self.map_load_obstacle.subsample(config.icon_path['size'])

        self.map_load_obstacle_explored     = PhotoImage(file=config.icon_path['explored_obstacle'])
        self.map_obstacle_explored          = self.map_load_obstacle_explored.subsample(config.icon_path['size'])

        # Pictures for Robot for the various orientation
        self.robot_size     = config.robot_parameters['size']
        self.robot_n = []
        self.robot_s = []
        self.robot_e = []
        self.robot_w = []
        for i in range(self.robot_size**2):
            self.robot_n += [PhotoImage(file=config.icon_path['north'][i]).subsample(config.icon_path['size'])]
            self.robot_s += [PhotoImage(file=config.icon_path['south'][i]).subsample(config.icon_path['size'])]
            self.robot_w += [PhotoImage(file=config.icon_path['west'][i]).subsample(config.icon_path['size'])]
            self.robot_e += [PhotoImage(file=config.icon_path['east'][i]).subsample(config.icon_path['size'])]
        
        
        #  Initialize Map
        self.current_map      = deepcopy(self.map.get_map())
        self.robot_location  = self.map.get_robot_location()
        self.robot_direction = self.map.get_robot_direction()
        self.update_map(init=True)
        
        #----------------------------------------------------------------------
        #Control Panel
        #----------------------------------------------------------------------
        control_pane_window = ttk.Panedwindow(self.control_pane, orient=VERTICAL)
        control_pane_window.grid(column=0, row=0, sticky=(N, S, E, W))

        condition_pane = ttk.Labelframe(control_pane_window, text='Special Conditions')
        control_pane_window.add(condition_pane, weight=4)
        
        action_pane = ttk.Labelframe(control_pane_window, text='Action')
        control_pane_window.add(action_pane, weight=1)

        #Control Panel Control Special Conditions
        #Speed in Steps/Second
        speed_label = ttk.Label(condition_pane, text = "Speed(in Steps Per Second):")
        speed_label.grid(column=0, row=0, sticky=W)
        self.speed_status = False
        self.speed_value = IntVar()
        self.speed = ttk.Combobox(condition_pane, textvariable = self.speed_value)
        self.speed['values'] = (1,2,3,4,5)
        self.speed.grid(column = 0, row = 1, pady =(0,10))
        
        
        #Coverage Figure in %
        coverage_label = ttk.Label(condition_pane, text="Coverage Figure(%):")
        coverage_label.grid(column=0, row=2, sticky=W)
        self.coverage_status = False
        self.coverage_value = IntVar()
        self.coverage = ttk.Combobox(condition_pane, textvariable = self.coverage_value)
        self.coverage['values'] = (10,20,30,40,50,60,70,80,90,100)
        self.coverage.grid(column=0, row=3, pady=(0, 10))
        
        #Time Limit in Second 
        time_label = ttk.Label(condition_pane, text="Time Limit(s):")
        time_label.grid(column=0, row=4, sticky=W)
        self.time_status = False
        self.time_value = StringVar()
        self.time = ttk.Combobox(condition_pane, textvariable = self.time_value)
        self.time['values'] = ("0:05","0:40","1:00","1:20","1:40","2:00","2:20","2:40","3:00")
        self.time.grid(column=0, row=5, pady=(0, 10))


        #Control Panel Action Commands
        explore_button = ttk.Button(action_pane, text='Explore', width=20, command=self.algo.explore)
        explore_button.grid(column=1, row=0, sticky=(W, E))
        
        fastest_path_button = ttk.Button(action_pane, text='Fastest Path', command=self.algo.run)
        fastest_path_button.grid(column=1, row=1, sticky=(W, E))
        
        move_button = ttk.Button(action_pane, text='Move', command=self.move)
        move_button.grid(column=1, row=3, sticky=(W, E))
        
        left_button = ttk.Button(action_pane, text='Left', command=self.left)
        left_button.grid(column=0, row=4, sticky=(W, E))

        right_button = ttk.Button(action_pane, text='Right', command=self.right)
        right_button.grid(column=2, row=4, sticky=(W, E))
        
        back_button = ttk.Button(action_pane, text='Back', command=self.back)
        back_button.grid(column=1, row=5, sticky=(W, E))

        actual_run_button = ttk.Button(action_pane, text='Actual Run', command=self.actual_run)
        actual_run_button.grid(column=1, row=6, sticky=(W, E))

        self.control_pane.columnconfigure(0, weight=1)
        self.control_pane.rowconfigure(0, weight=1)

        #Keybinding of Action Commands to allow keyboard control
        self.master.bind("<Up>", lambda e: self.move())
        self.master.bind("<Left>", lambda e: self.left())
        self.master.bind("<Right>", lambda e: self.right())
        self.master.bind("<Down>", lambda e: self.back())
        
        self.master.mainloop()

    def actual_run(self):
        self.handler.loop()
        self.master.after(200, self.actual_run)

    # ----------------------------------------------------------------------
    #   Actions received by robot
    # ----------------------------------------------------------------------
    def move(self):
        self.handler.move()
        self.update_map()

    def left(self):
        self.handler.left()
        self.update_map()

    def right(self):
        self.handler.right()
        self.update_map()

    def back(self):
        self.handler.back()
        self.update_map()

    # ----------------------------------------------------------------------
    # Special Conditions (for situations where user selected a special condition)
    # ----------------------------------------------------------------------
    def specified_speed(self):
        spd = int(self.speed.get())
        if (spd != 0):
            self.speed_status = True 
            return 

    def specified_coverage(self):
        cov = int(self.coverage.get())
        if (cov != 0):
            self.coverage_status =True
            return 
            
    def specified_time(self):
        t = str(self.time.get())
        if (t != ""):
            time = self.convert_time(t)
            self.time_status = True
            return time
        return 

    def convert_time(self, time):
        m, s = time.split(':')
        return int(m) * 60 + int(s)

    # ----------------------------------------------------------------------
    # Updating the map dynamically
    # ----------------------------------------------------------------------
    # Replace the area that Robot is on with Robot 
    def replace(self, x, y, direction):
        if direction == 'N':
            robot_image = self.robot_n
        elif direction == 'E':
            robot_image = self.robot_e
        elif direction == 'S':
            robot_image = self.robot_s
        else:
            robot_image = self.robot_w

        for i in range(self.robot_size):
            for j in range(self.robot_size):
                cell = ttk.Label(self.map_pane, image=robot_image[i*self.robot_size+j], borderwidth=1)
                try:
                    self.map_pane[x+i-1][y+j-1].destroy()
                except Exception:
                    pass
                cell.grid(column=y+j-1, row=x+i-1)
                self.map_widget[x+i-1][y+j-1] = cell

    # Replaces Map with updated one
    def replace_map(self, x, y):
        # Start & Goal areas
        if   ((0 <= y < 3) and(0 <= x < 3)):
                map_image = self.map_start
        elif ((self.map.length -3 <= y < self.map.length) and
              (self.map.width-3 <= x < self.map.width)):
                map_image = self.map_goal

        # Area Unexplored
        elif not self.map.isExplored(x,y):
            if self.map.isObstacle(x,y):
                map_image = self.map_obstacle
            else:
                map_image = self.map_free
        
        # Area Explored
        else:
            if self.map.isObstacle(x,y):
                map_image = self.map_obstacle_explored
            else:
                map_image = self.map_free_explored
            
        # Change map
        cell = ttk.Label(self.map_pane, image=map_image, borderwidth=1)
        try:
            self.map_pane[x][y].destroy()
        except Exception:
            pass
        cell.grid(column=y, row=x)
        self.map_widget[x][y] = cell

    # Updating the map
    def update_map(self, init=False):
        print ("updating map")
        start_time= time.time()
        if init:
            next_map = self.current_map
        else:
            next_map = self.map.get_map()
        next_robot_location  = self.map.get_robot_location()
        next_robot_direction = self.map.get_robot_direction()

        # if Robot position changed, change the space it was previously occupying back to map
        if self.robot_location != next_robot_location:
            for i in range(self.robot_location[0]-1, self.robot_location[0]+2):
                for j in range(self.robot_location[1]-1, self.robot_location[1]+2):
                    if not (next_robot_location[0]-1 <= i <= next_robot_location[0]+1 and
                            next_robot_location[1]-1 <= j <= next_robot_location[1]+1):
                        self.replace_map(i,j)
                        self.current_map[i][j] = next_map[i][j]

        # Map all changed grid and non-Robot area
        for i in range(self.map.width):
            for j in range(self.map.length):
                if (not (next_robot_location[0]-1 <= i <= next_robot_location[0]+1 and
                         next_robot_location[1]-1 <= j <= next_robot_location[1]+1) and
                        (init or self.current_map[i][j] != next_map[i][j])):
                    self.replace_map(i, j)
                    self.current_map[i][j] = next_map[i][j]

        # Place Robot on Map
        if (init or
            self.robot_location  != next_robot_location or
            self.robot_direction != next_robot_direction):
            self.replace(next_robot_location[0], next_robot_location[1], next_robot_direction)
        
        # Update change
        self.robot_location  = next_robot_location
        self.robot_direction = next_robot_direction
        print("updating map in", time.time()- start_time)
    # ----------------------------End of Class--------------------------------------------
#start simulator
sim = Simulator()



