from PyQt5.QtCore import QPointF


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
        try:
            self.points.pop(index)
            return self.vertexes.pop(index)
        except Exception:
            return None

    def pop_edge(self, index: int):
        try:
            return self.edges.pop(index)
        except Exception:
            return None