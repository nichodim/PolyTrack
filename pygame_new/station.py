class Station:
    def __init__(self, image, rect, point, orientation, id):
        self.type = "station"
        self.image = image
        self.rect = rect
        self.point = point
        self.orientation = orientation
        self.id = id