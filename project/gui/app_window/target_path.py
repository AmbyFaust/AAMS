from PyQt5.QtCore import QPointF
from PyQt5.QtWidgets import QWidget


class TargetPath:
    def __init__(self):
        self.vertexes = []
        self.points = []
        self.edges = []

    def add_vertex(self, obj, pos: QPointF):
        self.vertexes.append(obj)
        self.points.append(pos)

    def add_edge(self, obj):
        self.edges.append(obj)

    def pop_vertex(self, index: int):
        self.vertexes.pop(index)
        self.points.pop(index)
