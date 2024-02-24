from constants import *

TrackOffset = {
    'origin': (0, 0), 
    'up': (0, -TRACK_HEIGHT), 
    'down': (0, TRACK_HEIGHT), 
    'left': (-TRACK_WIDTH, 0), 
    'right': (TRACK_WIDTH, 0)
}

TrackSetTypes = {
    'straight': [
        ('origin', TrackSprites.vertical_track), 
        ('down', TrackSprites.vertical_track), 
        ('down', TrackSprites.vertical_track), 
        ('down', TrackSprites.vertical_track)
    ]
}