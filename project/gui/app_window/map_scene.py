from PyQt5.QtCore import Qt, QPoint, QSize, pyqtSlot, QTimer, pyqtSignal, QLine, QLineF
from PyQt5.QtGui import QPen, QPixmap, QCursor, QPainterPath, QColor, QIcon
from PyQt5.QtWidgets import QGraphicsScene, QGraphicsPixmapItem, QGraphicsSceneMouseEvent, QGraphicsEllipseItem, \
    QGraphicsLineItem

from project import ObjectEnum
from project.gui.app_window.controller import Controller
from project.gui.app_window.target_path import TargetPath
from project.settings import BASE_SIZE_OBJECT, SAR_ICON_PATH, TARGET_ICON_PATH, TARGET_POINT_RADIUS


class GridScene(QGraphicsScene):
    get_current_coordinates = pyqtSignal(int, int)

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
        self.current_line = None

        self.mouse_position_timer = QTimer()

    def draw_grid(self, rect: QSize):

        pen = QPen(Qt.gray)
        for x in range(0, rect.width() + 1, self.grid_size):
            self.addLine(x, 0, x, rect.height(), pen)
        for y in range(0, rect.height() + 1, self.grid_size):
            self.addLine(0, y, rect.width(), y, pen)

        # таймер для обновления координат мыши
        self.mouse_position_timer.timeout.connect(self.__update_mouse_position)
        self.mouse_position_timer.start(1)

    def mousePressEvent(self, event: QGraphicsSceneMouseEvent):
        if event.button() == Qt.LeftButton:
            if self.current_obj_type == ObjectEnum.SAR:
                if self.current_object is not None:
                    self.removeItem(self.current_object)
                self.__draw_sar(event)

            elif self.current_obj_type == ObjectEnum.TARGET:
                self.__draw_target_path(event)

        elif event.button() == Qt.RightButton:
            self.controller.create_object(self.current_obj_type, self.current_object)
            if self.current_obj_type == ObjectEnum.SAR:
                self.sars[self.sar_counter] = self.current_object
                self.sar_counter += 1
            elif self.current_obj_type == ObjectEnum.TARGET:
                last_point = self.current_object.points[-1]
                self.removeItem(self.current_object.pop_vertex(-1))
                last_vertex = QGraphicsEllipseItem(int(last_point.x()) - TARGET_POINT_RADIUS,
                                                  int(last_point.y()) - TARGET_POINT_RADIUS,
                                                  TARGET_POINT_RADIUS * 2, TARGET_POINT_RADIUS * 2)
                last_vertex.setBrush(QColor("red"))
                self.addItem(last_vertex)
                self.current_object.add_vertex(last_vertex, last_point)
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

    def __update_mouse_position(self):
        mouse_position = QCursor.pos()
        global_position = self.views()[0].mapFromGlobal(mouse_position)
        scene_position = self.views()[0].mapToScene(global_position)

        if (0 < scene_position.x() < self.sceneRect().width()) and (
                0 < scene_position.y() < self.sceneRect().height()):
            self.get_current_coordinates.emit(int(scene_position.x() - 1), int(scene_position.y() - 1))

    def __draw_target_path(self, event: QGraphicsSceneMouseEvent):
        if self.current_object is None:
            self.current_object = TargetPath()

            pixmap = QPixmap(TARGET_ICON_PATH)
            pixmap.scaled(BASE_SIZE_OBJECT)
            new_vertex = QGraphicsPixmapItem(pixmap)
            new_vertex.setScale(1)
            new_vertex.setPos(
                event.scenePos() - QPoint(BASE_SIZE_OBJECT.width() // 2, BASE_SIZE_OBJECT.height() // 2)
            )
            self.current_object.add_vertex(new_vertex, event.scenePos())
            self.addItem(new_vertex)
        else:
            new_edge = QLineF(self.current_object.points[-1], event.scenePos())
            self.addLine(new_edge, QPen(Qt.black, 3))
            self.current_object.add_edge(self.items()[0])


            new_vertex = QGraphicsEllipseItem(int(event.scenePos().x()) - TARGET_POINT_RADIUS,
                                              int(event.scenePos().y()) - TARGET_POINT_RADIUS,
                                              TARGET_POINT_RADIUS * 2, TARGET_POINT_RADIUS * 2)
            new_vertex.setBrush(QColor("black"))
            self.addItem(new_vertex)
            self.current_object.add_vertex(new_vertex, event.scenePos())

        self.update()

    def __draw_sar(self, event: QGraphicsSceneMouseEvent):
        pixmap = QPixmap(SAR_ICON_PATH)

        pixmap.scaled(BASE_SIZE_OBJECT)
        self.current_object = QGraphicsPixmapItem(pixmap)
        self.current_object.setScale(1)
        self.current_object.setPos(
            event.scenePos() - QPoint(BASE_SIZE_OBJECT.width() // 2, BASE_SIZE_OBJECT.height() // 2))
        self.addItem(self.current_object)


    @pyqtSlot(int, object)
    def remove_object(self, object_id: int, object_type: ObjectEnum):
        try:
            if object_type is ObjectEnum.TARGET:
                target_path = self.targets[object_id]
                self.__remove_target_path(target_path)
                del self.targets[object_id]

            elif object_type is ObjectEnum.SAR:
                self.__remove_sar(object_id)

        except BaseException as exp:
            print(f'Ошибка при удалении объекта "{object_type.desc}" с id = {object_id}: {exp}')

    def __remove_target_path(self, target_path: TargetPath):
        for vertex in target_path.vertexes:
            self.removeItem(vertex)
        for edge in target_path.edges:
            self.removeItem(edge)

    def __remove_sar(self, sar_id: int):
        self.removeItem(self.sars[sar_id])
        self.sars.pop(sar_id)

    @pyqtSlot(object, object)
    def redraw_object(self, object_entity: object, object_type: ObjectEnum):
        try:
            if object_type is ObjectEnum.TARGET:
                if object_entity.id not in self.targets:
                    return

                pixmap = QPixmap(TARGET_ICON_PATH)

                self.removeItem(self.targets[object_entity.id])

                pixmap.scaled(BASE_SIZE_OBJECT)
                redraw_target = QGraphicsPixmapItem(pixmap)
                redraw_target.setScale(1)
                redraw_target.setPos(
                    object_entity.coordinates.to_q_point() -
                    QPoint(BASE_SIZE_OBJECT.width() // 2, BASE_SIZE_OBJECT.height() // 2)
                )
                self.addItem(redraw_target)

                self.targets[object_entity.id] = redraw_target

            elif object_type is ObjectEnum.SAR:
                if object_entity.id not in self.sars:
                    return

                pixmap = QPixmap(SAR_ICON_PATH)

                self.removeItem(self.sars[object_entity.id])

                pixmap.scaled(BASE_SIZE_OBJECT)
                redraw_sar = QGraphicsPixmapItem(pixmap)
                redraw_sar.setScale(1)
                redraw_sar.setPos(
                    object_entity.coordinates.to_q_point() -
                    QPoint(BASE_SIZE_OBJECT.width() // 2, BASE_SIZE_OBJECT.height() // 2)
                )
                self.addItem(redraw_sar)

                self.sars[object_entity.id] = redraw_sar

            self.current_object = None
            self.current_obj_type = None
        except BaseException as exp:
            print(f'{exp}')
