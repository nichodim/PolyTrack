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
g, t, w, i, s = 'grass', 'tallgrass', 'water', 'ice', 'snow'
df, bul = 'default', 'bullet'

# Maps
GrassMapSmall = {
    'type': 'vanilla',
    'board': [ # map of board terrain
        [t,t,t,g,g,g,t,g,g,g], 
        [g,g,g,g,t,g,g,g,t,g], 
        [g,t,g,g,t,g,g,g,g,g], 
        [g,g,t,g,g,g,g,g,g,g], 
        [t,g,g,t,g,t,g,t,g,t], 
        [g,g,g,g,g,g,g,t,g,g], 
        [g,t,g,g,t,g,g,t,g,g], 
        [g,g,g,g,g,g,g,g,w,w], 
        [t,g,t,t,g,g,g,g,w,w], 
        [t,t,g,g,g,g,g,w,w,w], 
    ], 
    'obstacles': [ # obstacles to choose from
        'rock', 'sandrock', 'sadrock', 
        'tree', 'woodshack'
    ],
    'levels': [
        { # level
            'obstacle_range': (3, 4),
            'rounds': [
                [df, df], [df], [df, df], [df, df], [bul]
            ]
        }, 
        {
            'obstacle_range': (4, 6),
            'rounds': [
                [df], [df, df], [df], [df, df], [df, df]
            ]
        },
        {
            'obstacle_range': (7, 8),
            'rounds': [
                [df, df], [df], [df, df], [df, df], [bul]
            ]
        },
        {
            'obstacle_range': (7, 8),
            'rounds': [
                [df], [df, df], [df], [df, df], [df, df]
            ]
        },
        {
            'obstacle_range': (9, 10),
            'rounds': [
                [bul], [df, bul], [df, df], [bul, bul], [bul, bul]
            ]

        },
    ]
}

GrassMapMedium = {
    'type': 'vanilla',
    'board': [
        [g,g,g,w,w,w,w,w,g,g,g,g,g,g,g],
        [g,g,g,g,g,w,w,g,g,g,t,g,g,g,g],
        [g,g,g,g,g,g,g,g,g,g,g,t,t,t,g],
        [g,g,g,g,g,g,g,g,g,g,g,g,t,t,g],
        [g,g,g,g,g,g,g,g,g,g,g,g,g,g,g],
        [g,g,g,g,t,g,g,g,g,g,g,g,g,g,g],
        [g,g,g,t,t,g,g,g,g,g,g,g,g,g,g],
        [g,g,t,t,g,g,g,g,g,g,g,g,g,g,g],
        [w,w,w,g,g,g,g,g,g,w,w,w,g,g,g],
        [w,w,w,w,g,g,g,g,w,w,w,w,w,g,g],
    ],

    'obstacles': [
        'woodshack', 'sandrock', 'sadrock', "rock", 'tree'
    ],

    'levels': {
        {
            'obstacle_range': (5,7),
            'rounds': [
                [df, df], [df], [df, df], [df, df], [bul]
            ]
        },
        {
            'obstacle_range': (8, 9),
            'rounds': [
                [df], [df, df], [df], [df, df], [df, df]
            ]
        },
        {
            'obstacle_range': (10, 12),
            'rounds': [
                [df, df], [df], [df, df], [df, df], [bul]
            ]
        },
        {
            'obstacle_range': (12, 14),
            'rounds': [
                [df], [df, df], [df], [df, df], [df, df]
            ]
        },
        {
            'obstacle_range': (14, 15),
            'rounds': [
                [bul], [df, bul], [df, df], [bul, bul], [bul, bul]
            ]
        },
    }

}

GrassMapLarge = {
    'type': 'vanilla',
    'board': [
        [g,g,g,g,g,w,w,w,w,w,w,g,g,g,g,g,w,w,w,w],
        [g,g,g,g,g,g,g,w,w,w,g,g,g,g,g,g,w,w,w,w],
        [g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,w,w,w],
        [g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,w,w,w],
        [g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,w,w,w,w],
        [w,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,w,w,w,g],
        [w,g,g,g,g,g,g,g,g,g,g,g,g,g,g,g,w,w,w,g],
        [w,w,w,w,g,g,g,g,g,g,g,g,g,g,g,g,g,w,w,g],
        [w,w,w,w,w,g,g,g,g,g,g,w,w,g,g,g,g,g,g,g],
        [w,w,w,w,w,g,g,g,g,w,w,w,w,g,g,g,g,g,g,g],
        [w,w,w,w,w,g,g,g,w,w,w,w,w,w,g,g,g,g,g,g],
    ],

    'obstacles': [
        'woodshack', 'sandrock', 'sadrock', "rock", 'tree'
    ],

    'levels': [
        {
            'obstacle_range': (10, 14),
            'rounds': [
                [df], [df], [df, df], [df, df], [bul]
            ]
        },

        {
            'obstacle_range': (8, 12),
            'rounds': [
                [bul], [bul], [bul, df], [bul, df], [bul, df]
            ]
        },

        {
            'obstacle_range': (12, 14),
            'rounds': [
                [df, bul], [df, bul], [df, df, bul], [df, df, bul], [bul, bul]
            ]
        },

        {
            'obstacle_range': (12, 14),
            'rounds': [
                [df, bul], [df, bul], [df, df, bul], [df, df, bul], [bul, bul]
            ]
        },
        {
            'obstacle_range': (5, 15),
            'rounds': [
                [bul], [bul, bul], [df, bul, bul], [df, bul, bul], [bul, bul, bul]
            ]
        },
    ]
}

SnowMapSmall = {
    'type': 'snowy',
    'board': [
        [i,i,s,s,s,s,s,s,s,i],
        [i,i,s,s,s,s,s,s,s,i],
        [i,s,s,s,s,s,s,s,s,i],
        [s,s,s,s,s,s,s,i,i,i],
        [s,s,s,s,s,s,s,s,i,i],
        [s,s,s,s,s,s,s,s,s,i],
        [s,s,s,s,s,s,s,s,s,s],
        [i,s,s,s,s,s,s,s,s,s],
        [i,i,i,s,s,s,s,s,s,s],
        [i,i,i,s,s,s,s,s,s,s],
    ],

    'obstacles': [
        'woodshack', 'sadrock', 'sandrock'
    ],

    'levels': [
        { # level
            'obstacle_range': (3, 4),
            'rounds': [
                [df, df], [df], [df, df], [df, df], [bul]
            ]
        }, 
        {
            'obstacle_range': (4, 6),
            'rounds': [
                [df], [df, df], [df], [df, df], [df, df]
            ]
        },
        {
            'obstacle_range': (7, 8),
            'rounds': [
                [df, df], [df], [df, df], [df, df], [bul]
            ]
        },
        {
            'obstacle_range': (7, 8),
            'rounds': [
                [df], [df, df], [df], [df, df], [df, df]
            ]
        },
        {
            'obstacle_range': (9, 10),
            'rounds': [
                [bul], [df, bul], [df, df], [bul, bul], [bul, bul]
            ]

        },
    ]
}

SnowMapMedium = {
        'type': 'snowy',
    'board' : [
        [w,w,w,w,s,s,s,i,i,i,i,i,s,s,s],
        [w,w,w,w,s,s,s,i,i,i,i,i,s,s,s],
        [s,s,s,w,w,s,s,s,s,i,i,s,s,s,s],
        [s,s,s,s,s,s,s,s,s,s,s,s,s,s,s],
        [s,s,s,s,s,s,s,s,s,s,s,s,s,s,s],
        [i,s,s,s,s,s,s,s,s,s,s,s,s,s,s],
        [i,s,s,s,s,s,s,s,s,s,s,s,s,s,s],
        [i,i,s,s,s,s,s,s,s,s,s,i,s,s,s],
        [i,i,i,s,s,s,s,s,s,s,i,i,i,s,s],
        [i,i,i,s,s,s,s,s,i,i,i,i,i,s,s],
    ],

    'obstacles': [
        'woodshack', 'sadrock', 'sandrock'
    ],

    'levels': {
        {
            'obstacle_range': (5,7),
            'rounds': [
                [df, df], [df], [df, df], [df, df], [bul]
            ]
        },
        {
            'obstacle_range': (8, 9),
            'rounds': [
                [df], [df, df], [df], [df, df], [df, df]
            ]
        },
        {
            'obstacle_range': (10, 12),
            'rounds': [
                [df, df], [df], [df, df], [df, df], [bul]
            ]
        },
        {
            'obstacle_range': (12, 14),
            'rounds': [
                [df], [df, df], [df], [df, df], [df, df]
            ]
        },
        {
            'obstacle_range': (14, 15),
            'rounds': [
                [bul], [df, bul], [df, df], [bul, bul], [bul, bul]
            ]
        },
    }
}

SnowMapL = {  
        'type': 'snowy', 
    'board': [
        [i,i,i,i,s,s,s,s,s,s,s,s,s,i,i,i,i,i,i,i,],
        [i,i,i,s,s,s,s,s,s,s,s,s,s,s,s,i,i,i,i,i,],
        [i,i,s,s,s,s,i,s,s,s,s,s,s,s,s,s,s,i,i,i,],
        [s,s,s,s,s,s,i,i,s,s,s,s,s,s,s,s,s,s,s,i,],
        [s,s,s,s,s,s,s,s,s,s,s,s,s,s,s,s,s,s,s,s,],
        [s,s,s,s,s,s,s,s,s,s,s,s,s,s,i,s,s,s,s,s,],
        [s,s,s,s,s,s,s,s,s,s,s,s,s,s,i,i,s,s,s,s,],
        [s,s,s,s,s,s,s,s,s,s,s,s,s,s,s,i,s,s,s,s,],
        [s,s,s,s,s,i,i,i,i,s,s,s,s,s,s,s,s,s,s,s,],
        [s,s,s,i,i,i,i,i,i,s,s,s,s,s,s,s,s,s,s,s,],

    ],

    'obstacles': [
        'woodshack', 'sadrock', 'sandrock'
    ],

    'levels':[
        {
            'obstacle_range': (10, 14),
            'rounds': [
                [df], [df], [df, df], [df, df], [bul]
            ]
        },

        {
            'obstacle_range': (8, 12),
            'rounds': [
                [bul], [bul], [bul, df], [bul, df], [bul, df]
            ]
        },

        {
            'obstacle_range': (12, 14),
            'rounds': [
                [df, bul], [df, bul], [df, df, bul], [df, df, bul], [bul, bul]
            ]
        },

        {
            'obstacle_range': (12, 14),
            'rounds': [
                [df, bul], [df, bul], [df, df, bul], [df, df, bul], [bul, bul]
            ]
        },
        {
            'obstacle_range': (5, 15),
            'rounds': [
                [bul], [bul, bul], [df, bul, bul], [df, bul, bul], [bul, bul, bul]
            ]
        },
    ]
}