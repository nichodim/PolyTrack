# Contains all maps with all of their levels and tile layouts

# Map builder explanation
'''
MapName = {
    'type': Type of map, this is used to determine logic specific to a type of map like water freezing
            Allows for easy variation like small, medium, and large variants
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
    'type': 'vanilla',
    'board': [ # map of board terrain
        [g,g,g,g,g,g,g,g,g,g], 
        [g,g,g,g,g,g,g,g,g,g], 
        [g,g,w,g,g,g,w,g,g,g], 
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
        [ # level
            [(3, 4), [df]], # rounds
            [(3, 5), [df]], 
            [(2, 3), [df, df]], 
        ], 
        [ 
            [(4, 6), [df]],
            [(3, 5), [df, df, df, df, df, df, df, df, df, df]], 
            [(2, 3), [df, bul]], 
        ], 
    ]
}