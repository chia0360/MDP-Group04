icon_path = dict(
    north = ['images/robot/topleft.gif',
             'images/robot/topright.gif',
             'images/robot/bottomleft2.gif',
             'images/robot/bottomright2.gif'],
    east  = ['images/robot/topleft2.gif',
             'images/robot/topright.gif',
             'images/robot/bottomleft2.gif',
             'images/robot/bottomright.gif'],
    south = ['images/robot/topleft2.gif',
             'images/robot/topright2.gif',
             'images/robot/bottomleft.gif',
             'images/robot/bottomright.gif'],
    west  = ['images/robot/topleft.gif',
             'images/robot/topright2.gif',
             'images/robot/bottomleft.gif',
             'images/robot/bottomright2.gif'],
    
    free  				= 'images/gray.gif',
    obstacle 			= 'images/gray.gif',
    explored_free		= 'images/d_blue.gif',
    explored_obstacle	= 'images/d_red.gif',
    start               = 'images/yellow.gif',
    end                 = 'images/l_green.gif',
    size                = 1
)

map_detail 	= dict(
    height	= 15,
    width	= 20
)

robot_detail = dict (
    size	= 2,
    delay   = 500
)

sensor_range = dict (
    front_left      = 1,
    front_right     = 1,
    left            = 1,
    right           = 1
)

verbose = dict (
    silent      = 0,
    quiet       = 1,
    normal      = 2,
    debug       = 3,
    deepdebug   = 4
)
verboseLv = verbose['normal']

robot_simulation = True
