# Handles tracks

from constants import *

class Track:
    def __init__(self, image, rect, d0, d90, d180, d270):
        self.type = "track"
        self.image = image
        self.rect = rect
        self.d0 = d0
        self.d90 = d90
        self.d180 = d180
        self.d270 = d270

        self.relations = []

    # Knows what tracks are next to it in the set
    # Turned out unnecessary for movement but could be useful maybe?
    def set_relation(self, track):
        self.relations.append(track)

    def move(self, relative_position):
        self.rect.move_ip(relative_position)
