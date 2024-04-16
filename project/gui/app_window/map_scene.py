from PyQt5.QtCore import Qt, QPoint, QSize
from PyQt5.QtGui import QPen, QPixmap
from PyQt5.QtWidgets import QGraphicsScene, QGraphicsPixmapItem

from project import ObjectEnum
from project.gui.app_window.controller import Controller
from project.settings import BASE_SIZE_OBJECT, RLS_ICON_PATH


class GridScene(QGraphicsScene):
    def __init__(self, parent=None, controller: Controller = None):
        super().__init__(parent)
        self.controller = controller
        self.grid_size = 50
        self.current_obj_type = None
        self.rls = {}
        self.rls_counter = 0
        self.targets = {}
        self.target_counter = 0
        self.current_object = None

    def drawGrid(self, rect: QSize):
        pen = QPen(Qt.gray)
        for x in range(0, rect.width() + 1, self.grid_size):
            self.addLine(x, 0, x, rect.height(), pen)
        for y in range(0, rect.height()+1, self.grid_size):
            self.addLine(0, y, rect.width(), y, pen)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            if self.current_obj_type == ObjectEnum.RLS:
                if self.current_object is not None:
                    self.removeItem(self.current_object)
                self.drawRLS(event)

        if event.button() == Qt.RightButton:
            self.controller.create_object(self.current_obj_type, self.current_object)
            if self.current_obj_type == ObjectEnum.RLS:
                self.rls[self.rls_counter] = self.current_object
                self.rls_counter += 1
            elif self.current_obj_type == ObjectEnum.TARGET:
                self.targets[self.target_counter] = self.current_object
                self.target_counter += 1
            self.current_obj_type = None
            self.current_object = None

    def drawRLS(self, event):
        pixmap = QPixmap(RLS_ICON_PATH)
        pixmap.scaled(BASE_SIZE_OBJECT)
        self.current_object = QGraphicsPixmapItem(pixmap)
        self.current_object.setScale(1)
        self.current_object.setPos(event.scenePos() - QPoint(BASE_SIZE_OBJECT.width() // 2, BASE_SIZE_OBJECT.height() // 2))
        self.addItem(self.current_object)

