from PyQt5.QtCore import Qt, QPoint, QSize, pyqtSlot
from PyQt5.QtGui import QPen, QPixmap
from PyQt5.QtWidgets import QGraphicsScene, QGraphicsPixmapItem, QGraphicsSceneMouseEvent

from project import ObjectEnum
from project.gui.app_window.controller import Controller
from project.settings import BASE_SIZE_OBJECT, SAR_ICON_PATH, TARGET_ICON_PATH


class GridScene(QGraphicsScene):
    def __init__(self, parent=None, controller: Controller = None):
        super().__init__(parent)
        self.controller = controller
        self.grid_size = 50
        self.current_obj_type = None
        self.sars = {}
        self.sar_counter = 0
        self.targets = {}
        self.target_counter = 0
        self.current_object = None

    def draw_grid(self, rect: QSize):
        pen = QPen(Qt.gray)
        for x in range(0, rect.width() + 1, self.grid_size):
            self.addLine(x, 0, x, rect.height(), pen)
        for y in range(0, rect.height()+1, self.grid_size):
            self.addLine(0, y, rect.width(), y, pen)

    def mousePressEvent(self, event: QGraphicsSceneMouseEvent):
        if event.button() == Qt.LeftButton:
            if self.current_obj_type == ObjectEnum.SAR:
                if self.current_object is not None:
                    self.removeItem(self.current_object)
                self.__draw_object(event, ObjectEnum.SAR)

            elif self.current_obj_type == ObjectEnum.TARGET:
                if self.current_object is not None:
                    self.removeItem(self.current_object)
                self.__draw_object(event, ObjectEnum.TARGET)

        if event.button() == Qt.RightButton:
            self.controller.create_object(self.current_obj_type, self.current_object)
            if self.current_obj_type == ObjectEnum.SAR:
                self.sars[self.sar_counter] = self.current_object
                self.sar_counter += 1
            elif self.current_obj_type == ObjectEnum.TARGET:
                self.targets[self.target_counter] = self.current_object
                self.target_counter += 1
            self.current_obj_type = None
            self.current_object = None

    def keyPressEvent(self, event: QGraphicsSceneMouseEvent):
        if event.key() == Qt.Key_Escape:
            if self.current_object is not None:
                self.removeItem(self.current_object)
            self.current_obj_type = None
            self.current_object = None

        if event.key() == Qt.Key_Backspace:
            if self.current_object is not None:
                self.removeItem(self.current_object)

    def __draw_object(self, event: QGraphicsSceneMouseEvent, object_type: ObjectEnum):
        pixmap = None

        if object_type == ObjectEnum.TARGET:
            pixmap = QPixmap(TARGET_ICON_PATH)

        elif object_type == ObjectEnum.SAR:
            pixmap = QPixmap(SAR_ICON_PATH)

        if pixmap:
            pixmap.scaled(BASE_SIZE_OBJECT)
            self.current_object = QGraphicsPixmapItem(pixmap)
            self.current_object.setScale(1)
            self.current_object.setPos(
                event.scenePos() - QPoint(BASE_SIZE_OBJECT.width() // 2, BASE_SIZE_OBJECT.height() // 2))
            self.addItem(self.current_object)

        else:
            print(f'Не удалось отрисовать объект, неизвестный тип: {object_type.desc}')

    @pyqtSlot(int, object)
    def remove_object(self, object_id: int, object_type: object):
        try:
            if object_type == ObjectEnum.TARGET:
                if object_id not in self.targets:
                    return

                self.current_object = self.targets[object_id]
                self.removeItem(self.current_object)
                self.targets.pop(object_id)

            elif object_type == ObjectEnum.SAR:
                if object_id not in self.sars:
                    return

                self.current_object = self.sars[object_id]
                self.removeItem(self.current_object)
                self.sars.pop(object_id)

            self.current_object = None
            self.current_obj_type = None

        except BaseException as exp:
            print(f'')
