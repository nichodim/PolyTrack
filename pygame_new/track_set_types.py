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

# 1 is the default, the incremented numbers represent the rotated version of the set
# Be mindful that the track box styling will need adjustment for bigger sizes
# *** With current styling, keep types at a max of 3 track width/height ***
TrackSetTypes = {
    # straight
    'bigstraight-1': [
        ('origin', TrackSprites.vertical), 
        ('down', TrackSprites.vertical), 
        ('down', TrackSprites.vertical), 
        ('down', TrackSprites.vertical)
    ], 
    'bigstraight-2': [
        ('origin', TrackSprites.horizontal), 
        ('right', TrackSprites.horizontal), 
        ('right', TrackSprites.horizontal), 
        ('right', TrackSprites.horizontal)
    ], 
    'medstraight-1': [
        ('origin', TrackSprites.vertical), 
        ('down', TrackSprites.vertical), 
        ('down', TrackSprites.vertical), 
    ], 
    'medstraight-2': [
        ('origin', TrackSprites.horizontal), 
        ('right', TrackSprites.horizontal), 
        ('right', TrackSprites.horizontal), 
    ], 
    'smallstraight-1': [
        ('origin', TrackSprites.vertical), 
        ('down', TrackSprites.vertical)
    ], 
    'smallstraight-2': [
        ('origin', TrackSprites.horizontal), 
        ('right', TrackSprites.horizontal)
    ], 

    # turn
    'bigturn-1': [
        ('origin', TrackSprites.vertical), 
        ('up', TrackSprites.vertical), 
        ('up', TrackSprites.left), 
        ('left', TrackSprites.horizontal), 
        ('left', TrackSprites.horizontal)
    ], 
    'bigturn-2': [
        ('origin', TrackSprites.horizontal), 
        ('left', TrackSprites.horizontal), 
        ('left', TrackSprites.right), 
        ('down', TrackSprites.vertical), 
        ('down', TrackSprites.vertical)
    ], 
    'bigturn-3': [
        ('origin', TrackSprites.vertical), 
        ('down', TrackSprites.vertical), 
        ('down', TrackSprites.inverted_right), 
        ('right', TrackSprites.horizontal), 
        ('right', TrackSprites.horizontal)
    ], 
    'bigturn-4': [
        ('origin', TrackSprites.horizontal), 
        ('right', TrackSprites.horizontal), 
        ('right', TrackSprites.inverted_left), 
        ('up', TrackSprites.vertical), 
        ('up', TrackSprites.vertical)
    ], 
    'medturn-1': [
        ('origin', TrackSprites.vertical), 
        ('up', TrackSprites.left), 
        ('left', TrackSprites.horizontal)
    ], 
    'medturn-2': [
        ('origin', TrackSprites.horizontal), 
        ('left', TrackSprites.right), 
        ('down', TrackSprites.vertical)
    ], 
    'medturn-3': [
        ('origin', TrackSprites.vertical), 
        ('down', TrackSprites.inverted_right), 
        ('right', TrackSprites.horizontal)
    ], 
    'medturn-4': [
        ('origin', TrackSprites.horizontal), 
        ('right', TrackSprites.inverted_left), 
        ('up', TrackSprites.vertical)
    ], 
    'smallturn-1': [
        ('origin', TrackSprites.left)
    ], 
    'smallturn-2': [
        ('origin', TrackSprites.right)
    ], 
    'smallturn-3': [
        ('origin', TrackSprites.inverted_right)
    ], 
    'smallturn-4': [
        ('origin', TrackSprites.inverted_left)
    ], 

    # u
    'u-1': [
        ('origin', TrackSprites.left), 
        ('left', TrackSprites.right)
    ], 
    'u-2': [
        ('origin', TrackSprites.inverted_left), 
        ('up', TrackSprites.left)
    ], 
    'u-3': [
        ('origin', TrackSprites.inverted_right), 
        ('right', TrackSprites.inverted_left)
    ], 
    'u-3': [
        ('origin', TrackSprites.right), 
        ('down', TrackSprites.inverted_right)
    ], 

    # hook
    'hook-1': [
        ('origin', TrackSprites.left), 
        ('left', TrackSprites.horizontal)
    ], 
    'hook-2': [
        ('origin', TrackSprites.right), 
        ('right', TrackSprites.horizontal)
    ], 
    'hook-3': [
        ('origin', TrackSprites.inverted_right), 
        ('up', TrackSprites.vertical)
    ], 
    'hook-4': [
        ('origin', TrackSprites.inverted_left), 
        ('down', TrackSprites.vertical)
    ], 

    # zigzag
    'zigzag-1': [
        ('origin', TrackSprites.vertical), 
        ('down', TrackSprites.inverted_right), 
        ('right', TrackSprites.left), 
        ('down', TrackSprites.vertical)
    ], 
    'zigzag-2': [
        ('origin', TrackSprites.horizontal), 
        ('right', TrackSprites.inverted_left), 
        ('up', TrackSprites.right), 
        ('right', TrackSprites.horizontal)
    ]
}

# Add multiple times to increase chances
SpawnTracks = [
    TrackSetTypes['medstraight-1'], 
    TrackSetTypes['smallstraight-1'], 
    TrackSetTypes['smallstraight-1'], 

    TrackSetTypes['medturn-1'], 
    TrackSetTypes['medturn-1'], 
    TrackSetTypes['smallturn-1'], 

    TrackSetTypes['u-1'], 
    TrackSetTypes['hook-1'], 
    TrackSetTypes['hook-1'], 
    TrackSetTypes['zigzag-1']
]