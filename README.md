#PolyTracks

The objective of this project was to experience the creation of a game using Agile methodologies, GitLab, and the use of Evolutionary Modeling.
Within this project, the user can jump into a PyGame that will allow them to have a variety of choices when selecting a potential map to play.
There are different map terrains and a variety of sizes. A brief introduction to the map creation can be seen below.
''' python
# Map builder explanation
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
map_types = ['vanilla', 'frozen'] # Make sure to use these for types

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
                [df], [df], [df, df], [df, df], [bul]
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
            'obstacle_range': (35, 40),
            'rounds': [
                [df], [df], [df], [df, df], [df], [bul]
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
'''
