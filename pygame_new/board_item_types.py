from constants import *
from track_set_types import *

# Data for attached items to tiles and board in general
# Use these to build logic around the board

TerrainTypes = {
    'grass': None, 
    'sand': None, 
    'water': None
}

TrackTypes = [vertical, horizontal, left, right, ileft, iright]

TrainTypes = {
    'default': {
        'image': TrainSprites.red_train,
        'speed': 0.15
    }
}

ObstacleTypes = {
    'rock': ObstacleSprites.rock, 
    'sandrock': ObstacleSprites.sandrock, 
    'sadrock': ObstacleSprites.sadrock, 
    'tree': ObstacleSprites.tree, 
    'woodshack': ObstacleSprites.woodshack
}
SpawnObstacles = [
    'rock', 'sandrock', 'sadrock', 
    'tree', 'woodshack'
]