from constants import *

width_and_gap = TRACK_WIDTH + INNER_GAP
height_and_gap = TRACK_HEIGHT + INNER_GAP

TrackOffset = {
    'origin': (0, 0), 
    'up': (0, -height_and_gap), 
    'down': (0, height_and_gap), 
    'left': (-width_and_gap, 0), 
    'right': (width_and_gap, 0)
}

# base case for tracks
vertical = {
    'name': 'vertical', 
    'sprite': TrackSprites.vertical, 
    'directions': ["crash", "forward", "crash", "forward"]
}
horizontal = {
    'name': 'horizontal', 
    'sprite': TrackSprites.horizontal, 
    'directions': ["forward", "crash", "forward", "crash"]
}
left = {
    'name': 'left', 
    'sprite': TrackSprites.left, 
    'directions': ["clockwise", "counter-clockwise", "crash", "crash"]
}
right = {
    'name': 'right', 
    'sprite': TrackSprites.right, 
    'directions': ["crash", "clockwise", "counter-clockwise", "crash"]
}
ileft = {
    'name': 'ileft', 
    'sprite': TrackSprites.inverted_left, 
    'directions': ["counter-clockwise", "crash", "crash", "clockwise"]
}
iright = {
    'name': 'iright', 
    'sprite': TrackSprites.inverted_right, 
    'directions': ["crash", "crash", "clockwise", "counter-clockwise"]
}

# 1 is the default, the incremented numbers represent the rotated version of the set
# Be mindful that the track box styling will need adjustment for bigger sizes
# *** With current styling, keep types at a max of 3 track width/height ***
TrackSetTypes = {
    # straight
    'bigstraight-1': [
        ('origin', vertical), 
        ('down', vertical), 
        ('down', vertical), 
        ('down', vertical)
    ], 
    'bigstraight-2': [
        ('origin', horizontal), 
        ('right', horizontal), 
        ('right', horizontal), 
        ('right', horizontal)
    ], 
    'medstraight-1': [
        ('origin', vertical), 
        ('down', vertical), 
        ('down', vertical), 
    ], 
    'medstraight-2': [
        ('origin', horizontal), 
        ('right', horizontal), 
        ('right', horizontal), 
    ], 
    'smallstraight-1': [
        ('origin', vertical), 
        ('down', vertical)
    ], 
    'smallstraight-2': [
        ('origin', horizontal), 
        ('right', horizontal)
    ], 
    'tinystraight-1': [
        ('origin', vertical)
    ], 
    'tinystraight-2': [
        ('origin', horizontal)
    ], 

    # turn
    'leftturn-1': [
        ('origin', vertical), 
        ('up', left), 
        ('left', horizontal)
    ], 
    'leftturn-2': [
        ('origin', horizontal), 
        ('left', right), 
        ('down', vertical)
    ], 
    'leftturn-3': [
        ('origin', vertical), 
        ('down', iright), 
        ('right', horizontal)
    ], 
    'leftturn-4': [
        ('origin', horizontal), 
        ('right', ileft), 
        ('up', vertical)
    ], 

    'rightturn-1': [
        ('origin', vertical), 
        ('up', right), 
        ('right', horizontal)
    ], 
    'rightturn-2': [
        ('origin', horizontal), 
        ('right', left), 
        ('down', vertical)
    ], 
    'rightturn-3': [
        ('origin', vertical), 
        ('down', ileft), 
        ('left', horizontal)
    ], 
    'rightturn-4': [
        ('origin', horizontal), 
        ('left', iright), 
        ('up', vertical)
    ], 

    'smallturn-1': [
        ('origin', left)
    ], 
    'smallturn-2': [
        ('origin', right)
    ], 
    'smallturn-3': [
        ('origin', iright)
    ], 
    'smallturn-4': [
        ('origin', ileft)
    ], 

    # u
    'u-1': [
        ('origin', left), 
        ('left', right)
    ], 
    'u-2': [
        ('origin', ileft), 
        ('up', left)
    ], 
    'u-3': [
        ('origin', iright), 
        ('right', ileft)
    ], 
    'u-4': [
        ('origin', right), 
        ('down', iright)
    ], 

    # hook
    'lefthook-1': [
        ('origin', left), 
        ('left', horizontal)
    ], 
    'lefthook-2': [
        ('origin', ileft), 
        ('up', vertical)
    ], 
    'lefthook-3': [
        ('origin', iright), 
        ('right', horizontal)
    ], 
    'lefthook-4': [
        ('origin', right), 
        ('down', vertical)
    ], 

    'righthook-1': [
        ('origin', right), 
        ('right', horizontal)
    ], 
    'righthook-2': [
        ('origin', iright), 
        ('up', vertical)
    ], 
    'righthook-3': [
        ('origin', ileft), 
        ('left', horizontal)
    ], 
    'righthook-4': [
        ('origin', left), 
        ('down', vertical)
    ], 

    'doublehook1-1': [
        ('origin', right), 
        ('right', ileft)
    ], 
    'doublehook1-2': [
        ('origin', iright), 
        ('up', left)
    ], 
    'doublehook1-3': [
        ('origin', ileft), 
        ('left', right)
    ], 
    'doublehook1-4': [
        ('origin', left), 
        ('down', iright)
    ], 
    
    # Modified by Kelvin Huang, April 29, 2024
    #
    # \__
    #    |
    'doublehook2-1': [
        ('origin', iright), 
        ('right', left)
    ], 
    'doublehook2-2': [
        ('origin', ileft), 
        ('up', right)
    ], 
    'doublehook2-3': [
        ('origin', left), 
        ('left', iright)
    ], 
    'doublehook2-4': [
        ('origin', right), 
        ('down', ileft)
    ], 
    
    # zigzag
    'zigzag-1': [
        ('origin', vertical), 
        ('down', iright), 
        ('right', left), 
        ('down', vertical)
    ], 
    'zigzag-2': [
        ('origin', horizontal), 
        ('right', ileft), 
        ('up', right), 
        ('right', horizontal)
    ],

    # Diagonal 
    'diagonal-1': [
        ('origin', right),
        ('right', ileft),
        ('up', right),
        ('right', ileft)
    ],
    'diagonal-2': [
        ('origin', left),
        ('left', iright),
        ('up', left),
        ('left', iright)
    ],
    'diagonal-3': [
        ('origin', ileft),
        ('up', right),
        ('right', ileft),
        ('up', right)
    ],
    'diagonal-4': [
        ('origin', iright),
        ('up', left),
        ('left', iright),
        ('up', left)
    ],
}

# Add multiple times to increase chances
SpawnTracks = [
    # Modified by Kelvin Huang, April 28, 2024
    # removed tracks that are basically the same except in different rotation
    # so that the new randomly generated track system feels more fair
    
    TrackSetTypes['medstraight-1'], 
    TrackSetTypes['smallstraight-1'], 
    TrackSetTypes['tinystraight-1'], 

    TrackSetTypes['leftturn-1'], 
    TrackSetTypes['smallturn-1'], 

    TrackSetTypes['u-1'], 
    TrackSetTypes['lefthook-1'], 
    TrackSetTypes['righthook-1'], 
    TrackSetTypes['doublehook1-1'],
    TrackSetTypes['doublehook2-1'],
    TrackSetTypes['zigzag-1'],
    TrackSetTypes['diagonal-1'],
]