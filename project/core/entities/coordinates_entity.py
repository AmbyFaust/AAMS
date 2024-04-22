from PyQt5.QtCore import QPoint


class CoordinatesEntity:
    def __init__(self, x: int = None, y: int = None):
        self.x = x
        self.y = y

    def to_q_point(self):
        return QPoint(self.x, self.y)
