from PyQt5.QtCore import Qt, QPoint, QSize
from PyQt5.QtGui import QPen
from PyQt5.QtWidgets import QGraphicsScene


class GridScene(QGraphicsScene):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.grid_size = 50

    def drawGrid(self, rect: QSize):
        pen = QPen(Qt.gray)
        for x in range(0, rect.width() + 1, self.grid_size):
            self.addLine(x, 0, x, rect.height(), pen)
        for y in range(0, rect.height()+1, self.grid_size):
            self.addLine(0, y, rect.width(), y, pen)