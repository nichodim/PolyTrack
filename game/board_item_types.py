from constants import *
from track_set_types import *

# Data for attached items to tiles and board in general
# Use these to build logic around the board

TerrainTypes = {
    'grass': TerrainSprites.grass,
    'tallgrass': TerrainSprites.tallgrass,
    'water': TerrainSprites.water, 
    'ice': TerrainSprites.ice,
    'snow': TerrainSprites.snow
}

TrackTypes = [vertical, horizontal, left, right, ileft, iright]

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

TrainTypes = {
    'default': {
        'image': TrainSprites.propane_cargo,
        'speed': 0.15,
    }, 
    'bullet': {
        'image': TrainSprites.gray_cargo,
        'speed': 0.25,
    }
}
TrainSpeed_Multipliers = {
    'fast_forward': {
        'multiplier': 8, 
        'active': False
    }, 
    'ice': {
        'multiplier': 1.15, 
        'active': False
    }, 
    'freeze': {
        'multiplier': 0.00001, 
        'active': False, 
        'time-limit': 150
    }, 
    'deep-freeze': { # Freeze but supposed to last longer
        'multiplier': 0.00001, 
        'active': False, 
        'time-limit': 300
    }, 
    'slow': {
        'multiplier': 0.35, 
        'active': False
    }
}