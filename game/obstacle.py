import random
from constants import *
from board_item_types import ObstacleTypes

class Obstacle:
    def __init__(self, obstacle_choices):
        self.type = random.choice(obstacle_choices)
        self.image = ObstacleTypes[self.type]