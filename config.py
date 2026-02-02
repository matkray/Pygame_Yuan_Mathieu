import constants

current_page = 0
max_pages = 1
check_wind = True

# Game settings
current_character = "redhat"
current_backdrop = "nature"
sound_volume = 0.50
sound_enabled = True

"""#page one platforms::###############################
platforms = [
    [
        #left:
        [0,0,50, constants.HEIGHT],

        #center:
        [50, constants.HEIGHT - 40, constants.WIDTH - 100, 40], #bottom side border
        [0,-50,constants.WIDTH, 70],
        [200, 700, 200, 400],
        [800, 200, 200, 500],
        [500, 400, 200, 200, -200],

        #right:
        [constants.WIDTH - 70,0,70, 0.5*constants.HEIGHT], #right side border
        [constants.WIDTH - 70,0.7*constants.HEIGHT,70, 0.4*constants.HEIGHT], #right side border
    ],
    [
        #left:
        [0,0,70, 0.5*constants.HEIGHT],
        [0,0.7*constants.HEIGHT,70, 0.4*constants.HEIGHT],

        #center:
        [70, constants.HEIGHT - 49, 0.5 * constants.WIDTH, 50],
        #[0.5 * constants.WIDTH, constants.HEIGHT - 99, 0.5 * constants.WIDTH, 100],
        [200, 700, 200, 100],
        [800, 200, 200, 100],
        [500, 400, 200, 100],

        #right:
        [constants.WIDTH - 40,0,40, 0.5*constants.HEIGHT], #right side border
        [constants.WIDTH - 40,0.85*constants.HEIGHT,40, 0.4*constants.HEIGHT], #right side border
    ],
    [
        [0,0,60, 0.5*constants.HEIGHT],
        [0,0.7*constants.HEIGHT,60, 0.4*constants.HEIGHT],

        [0, constants.HEIGHT - 49, 0.5 * constants.WIDTH, 50],
        [0.5 * constants.WIDTH, constants.HEIGHT - 99, 0.5 * constants.WIDTH, 100],
        [200, 700, 200, 100],
        [800, 200, 200, 100],
        [500, 400, 200, 100],
    ]
]
# end page one platforms::##########################"""