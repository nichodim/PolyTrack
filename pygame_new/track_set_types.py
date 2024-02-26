from constants import *

TrackOffset = {
    'origin': (0, 0), 
    'up': (0, -TRACK_HEIGHT - INNER_GAP), 
    'down': (0, TRACK_HEIGHT + INNER_GAP), 
    'left': (-TRACK_WIDTH - INNER_GAP, 0), 
    'right': (TRACK_WIDTH + INNER_GAP, 0)
}

TrackSetTypes = {
    'straight': [
        ('origin', TrackSprites.vertical_track), 
        ('down', TrackSprites.vertical_track), 
        ('down', TrackSprites.vertical_track), 
        ('down', TrackSprites.vertical_track)
    ], 
    'bigleft': [
        ('origin', TrackSprites.vertical_track), 
        ('up', TrackSprites.vertical_track), 
        ('up', TrackSprites.left_track), 
        ('left', TrackSprites.horizontal_track), 
        ('left', TrackSprites.horizontal_track)
    ]
}