import random
from constants import *
from board_item_types import ObstacleTypes, SpawnObstacles

class Obstacle:
    def __init__(self, type = None):
        if type: self.type = type
        else: self.type = random.choice(SpawnObstacles)

        self.image = ObstacleTypes[self.type]