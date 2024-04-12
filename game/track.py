# Handles tracks

from constants import *

class Track:
    def __init__(self, rect, data):
        self.rect = rect
        self.data = data
        self.image = data['sprite']
        self.directions = data['directions']

        self.relations = []

    # Knows what tracks are next to it in the set
    # Turned out unnecessary for movement but could be useful maybe?
    def set_relation(self, track):
        self.relations.append(track)

    def move(self, relative_position):
        self.rect.move_ip(relative_position)
