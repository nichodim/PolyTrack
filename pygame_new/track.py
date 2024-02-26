# Handles tracks

from constants import *

class Track:
    def __init__(self, image, rect):
        self.image = image
        self.rect = rect
        self.relations = []

    # Knows what tracks are next to it in the set
    # Turned out unnecessary for movement but could be useful maybe?
    def set_relation(self, track):
        self.relations.append(track)

    def move(self, relative_position):
        self.rect.move_ip(relative_position)
