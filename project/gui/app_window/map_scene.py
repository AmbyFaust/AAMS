from PyQt5.QtCore import Qt, QPoint, QSize, QEvent, QObject
from PyQt5.QtGui import QPen, QCursor, QPixmap
from PyQt5.QtWidgets import QGraphicsScene

from project.gui.app_window.controller import Controller
from project.gui.enums import ObjectEnum
from project.settings import BASE_SIZE_OBJECT, RLS_ICON_PATH


class GridScene(QGraphicsScene):
    def __init__(self, parent=None, controller: Controller = None):
        super().__init__(parent)
        self.controller = controller
        self.grid_size = 50
        self.current_obj = None

    def drawGrid(self, rect: QSize):
        pen = QPen(Qt.gray)
        for x in range(0, rect.width() + 1, self.grid_size):
            self.addLine(x, 0, x, rect.height(), pen)
        for y in range(0, rect.height()+1, self.grid_size):
            self.addLine(0, y, rect.width(), y, pen)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            if self.current_obj == ObjectEnum.RLS:
                self.drawRLS(event)

        if event.button() == Qt.RightButton:
            self.controller.create_object(self.current_obj)
            self.current_obj = None



    def drawRLS(self, event):
        pixmap = QPixmap(RLS_ICON_PATH)
        center_x = event.scenePos().x() - BASE_SIZE_OBJECT.width()/2
        center_y = event.scenePos().y() - BASE_SIZE_OBJECT.height()/2
        self.addPixmap(pixmap.scaled(BASE_SIZE_OBJECT)).setPos(center_x, center_y)

