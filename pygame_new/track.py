# Handles tracks

class Track:
    def __init__(self, image, rect):
        self.image = image
        self.rect = rect

    def move_track(self, relative_position):
        self.rect.move_ip(relative_position)