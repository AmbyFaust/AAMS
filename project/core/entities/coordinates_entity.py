from PyQt5.QtCore import QPoint
from collections import namedtuple

from project import settings


class CoordinatesEntity:
    def __init__(self, x: int = None, y: int = None, z: int = settings.HEIGHT):
        self.x = x
        self.y = y
        self.z = z

    def to_q_point(self):
        return QPoint(self.x, self.y)
