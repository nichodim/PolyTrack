# Contains all maps with all of their levels and tile layouts

# Map builder explanation
'''
MapName = {
    'type': Type of map, this is used to determine logic specific to a type of map like water freezing
            Allows for easy variation like small, medium, and large variants
    'board': Grid of tile terrain. Must have uniform row and col number
    'obstacles': List of spawnable obstacles on map (good for themes)
    'levels': Contains list of each level
              Each level contains an obstacle range and list of rounds
              Each round contains a list of trains to spawn
}
'''

# Abreviate anything to make larger maps easier (terrain should be uniform letter count)
from board_item_types import *
g, t, w = 'grass', 'tallgrass', 'water'
df, bul = 'default', 'bullet'

# Maps
VanillaMap = {
    'type': 'vanilla',
    'board': [ # map of board terrain
        [t,t,t,g,g,g,g,g,g,g], 
        [g,g,g,g,g,g,g,g,g,g], 
        [g,g,w,g,t,g,w,g,g,g], 
        [g,g,g,g,g,g,g,g,g,g], 
        [g,g,w,w,w,w,w,g,g,g], 
        [g,g,g,g,g,g,g,g,g,g], 
        [g,g,g,g,g,w,g,g,g,g], 
        [g,g,g,g,g,g,g,g,g,g], 
        [g,g,g,g,g,g,g,g,g,g], 
        [g,g,g,g,g,g,g,w,w,w], 
    ], 
    'obstacles': [ # obstacles to choose from
        'rock', 'sandrock', 'sadrock', 
        'tree', 'woodshack'
    ],
    'levels': [
        { # level
            'obstacle_range': (3, 4),
            'rounds': [
                [df], [df], [df, df]
            ]
        }
    ]
}