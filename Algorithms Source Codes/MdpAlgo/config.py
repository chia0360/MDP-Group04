map_dimensions  = dict(width = 15, length = 20)

robot_parameters = dict (size = 3, delay = 500)

sensor_range = dict (
    front_middle    = 4,
    front_left      = 3,
    front_right     = 3,
    left            = 3,
    right           = 3
)
icon_path = dict(
    north = ['images/robot/North1.gif',
             'images/robot/North2.gif',
             'images/robot/North3.gif',
             'images/robot/North4.gif',
             'images/robot/North5.gif',
             'images/robot/North6.gif',
             'images/robot/North7.gif',
             'images/robot/North8.gif',
             'images/robot/North9.gif'],
    east  = ['images/robot/East1.gif',
             'images/robot/East2.gif',
             'images/robot/East3.gif',
             'images/robot/East4.gif',
             'images/robot/East5.gif',
             'images/robot/East6.gif',
             'images/robot/East7.gif',
             'images/robot/East8.gif',
             'images/robot/East9.gif',],
    south = ['images/robot/South1.gif',
             'images/robot/South2.gif',
             'images/robot/South3.gif',
             'images/robot/South4.gif',
             'images/robot/South5.gif',
             'images/robot/South6.gif',
             'images/robot/South7.gif',
             'images/robot/South8.gif',
             'images/robot/South9.gif',],
    west  = ['images/robot/West1.gif',
             'images/robot/West2.gif',
             'images/robot/West3.gif',
             'images/robot/West4.gif',
             'images/robot/West5.gif',
             'images/robot/West6.gif',
             'images/robot/West7.gif',
             'images/robot/West8.gif',
             'images/robot/West9.gif',],
    
    free                = 'images/unexplored.gif',
    obstacle 		= 'images/unexplored.gif',
    explored_free	= 'images/free.gif',
    explored_obstacle	= 'images/block.gif',
    start               = 'images/Start.gif',
    end                 = 'images/Goal.gif',
    size                = 1
)



verbose = dict (
    silent      = 0,
    quiet       = 1,
    normal      = 2,
    debug       = 3,
    deepdebug   = 4
)

verboseLv = verbose['silent']

robot_simulation = True
