from constants import *

# Data for attached items to tiles and board in general
# Use these to build logic around the board

TerrainTypes = {
    'grass': None, 
    'sand': None, 
    'water': None
}

TrackTypes = {
    'horizontal': {'open': ('left', 'right'), 'sprite': TrackSprites.horizontal},
    'vertical': {'open': ('bottom', 'top'), 'sprite': TrackSprites.vertical},
    'right': {'open': ('bottom', 'right'), 'sprite': TrackSprites.right},
    'left': {'open': ('bottom', 'left'), 'sprite': TrackSprites.left},
    'inverted_right': {'open': ('top', 'right'), 'sprite': TrackSprites.inverted_right},
    'inverted_left': {'open': ('top', 'left'), 'sprite': TrackSprites.inverted_left},
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