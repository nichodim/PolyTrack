# Contains all maps with all of their levels and tile layouts

# Map builder explanation
'''
MapName = {
    'board': Grid of tile terrain. Must have uniform row and col number
    'obstacles': List of spawnable obstacles on map (good for themes)
    'levels': Contains list of each level
              Each level contains a list of rounds
              Each round constains... [obstacle spawn range, list of trains]
}
'''

# Abreviate anything to make larger maps easier (terrain should be uniform letter count)
from board_item_types import *
g, w = 'grass', 'water'
df, bul = 'default', 'bullet'

# Maps
VanillaMap = {
    'board': [ # map of board terrain
        [g,g,g,g,g,g,g,g,g,g], 
        [g,g,g,g,g,g,g,g,g,g], 
        [g,g,g,g,g,g,g,g,g,g], 
        [g,g,g,g,g,g,g,g,g,g], 
        [g,g,g,g,g,g,g,g,g,g], 
        [g,g,g,g,g,g,g,g,g,g], 
        [g,g,g,g,g,g,g,g,g,g], 
        [g,g,g,g,g,g,g,g,g,g], 
        [g,g,g,g,g,g,g,g,g,g], 
        [g,g,g,g,g,g,g,g,g,g], 
    ], 
    'obstacles': [ # obstacles to choose from
        'rock', 'sandrock', 'sadrock', 
        'tree', 'woodshack'
    ],
    'levels': [
        [ # level
            [(3, 4), [df]], # rounds
            [(3, 5), [df]], 
            [(2, 3), [df, df]], 
        ], 
    ]
}