class Coord(object):
    def __init__(self, x1=0, y1=0, x2=0, y2=0, name="", percent_accuracy=0.0):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.x_mid = (x1 + x2) / 2,
        self.y_mid = (y1 + y2) / 2,
        self.name = name
        self.percent_accuracy = percent_accuracy