import logging

from PyQt5.QtCore import Qt, QPoint, QSize, pyqtSlot, QTimer, pyqtSignal, QLineF, QRectF
from PyQt5.QtGui import QPen, QPixmap, QCursor, QColor
from PyQt5.QtWidgets import QGraphicsScene, QGraphicsPixmapItem, QGraphicsSceneMouseEvent, QGraphicsEllipseItem, \
    QGraphicsSceneWheelEvent

from project import ObjectEnum
from project.core import RadarEntity
from project.gui.app_window.controller import Controller
from project.gui.objects import TargetPath, RadarObject

from project.settings import BASE_SIZE_OBJECT, RADAR_ICON_PATH, TARGET_ICON_PATH, TARGET_POINT_RADIUS


class GridScene(QGraphicsScene):
    get_current_coordinates = pyqtSignal(int, int)

    def __init__(self, parent=None, controller: Controller = None):
        super().__init__(parent)
        self.controller = controller
        self.grid_size = 50
        self.radars = {}
        self.radar_counter = 0
        self.targets = {}
        self.target_counter = 0
        self.current_object = None
        self.current_obj_type = None

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
            if self.current_obj_type is ObjectEnum.RADAR:
                self.__draw_radar(event)

            elif self.current_obj_type is ObjectEnum.TARGET:
                self.__draw_target_path(event)

        elif event.button() == Qt.RightButton:
            self.controller.create_object(self.current_obj_type, self.current_object)
            if self.current_obj_type is ObjectEnum.RADAR:
                self.radars[self.radar_counter] = self.current_object
                self.radar_counter += 1
            elif self.current_obj_type is ObjectEnum.TARGET:
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
            if self.current_obj_type is ObjectEnum.RADAR:
                try:
                    self.removeItem(self.current_object.radar_item)
                    self.removeItem(self.current_object.radar_radius_item)
                except:
                    pass
            elif self.current_obj_type is ObjectEnum.TARGET:
                self.__remove_target_path(self.current_object)
            self.current_obj_type = None
            self.current_object = None

        if event.key() == Qt.Key_Backspace:
            if self.current_object is not None:
                if self.current_obj_type is ObjectEnum.RADAR:
                    try:
                        self.removeItem(self.current_object.radar_item)
                        self.removeItem(self.current_object.radar_radius_item)
                    except:
                        pass
                elif self.current_obj_type is ObjectEnum.TARGET:
                    self.removeItem(self.current_object.pop_vertex(-1))
                    self.removeItem(self.current_object.pop_edge(-1))

    def remove_from_map(self, current_object: object):
        try:
            if isinstance(current_object, TargetPath):
                self.__remove_target_path(current_object)
            elif isinstance(current_object, RadarObject):
                self.removeItem(current_object.radar_item)
                self.removeItem(current_object.radar_radius_item)
            self.current_obj_type = None
            self.current_object = None
        except BaseException as exp:
            print(exp)

    def __update_mouse_position(self):
        mouse_position = QCursor.pos()
        global_position = self.views()[0].mapFromGlobal(mouse_position)
        scene_position = self.views()[0].mapToScene(global_position)

        if (0 < scene_position.x() < self.sceneRect().width()) and (
                0 < scene_position.y() < self.sceneRect().height()):
            self.get_current_coordinates.emit(int(scene_position.x() - 1), int(scene_position.y() - 1))

    def __draw_target_path(self, event: QGraphicsSceneMouseEvent):
        if self.current_object is None or len(self.current_object.vertexes) == 0:
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

    def __draw_radar(self, event: QGraphicsSceneMouseEvent):
        try:
            if self.current_object is not None:
                self.removeItem(self.current_object.radar_item)
                self.removeItem(self.current_object.radar_radius_item)

            self.current_object = RadarObject()

            self.current_object.radar_item.setPos(
                event.scenePos() - QPoint(BASE_SIZE_OBJECT.width() // 2, BASE_SIZE_OBJECT.height() // 2))
            self.addItem(self.current_object.radar_item)

            self.current_object.radius_path.addEllipse(QRectF(-self.current_object.radius,
                                                              -self.current_object.radius,
                                                              2 * self.current_object.radius,
                                                              2 * self.current_object.radius))

            self.current_object.radar_radius_item = self.addPath(self.current_object.radius_path, QPen(Qt.blue))

            self.current_object.radar_radius_item.setPos(event.scenePos())
        except BaseException as exp:
            print(f'Ошибка нанесения рлс на карту: {exp}')

    @pyqtSlot(int, object)
    def remove_object(self, object_id: int, object_type: ObjectEnum):
        try:
            if object_type is ObjectEnum.TARGET:
                self.__remove_target(object_id)
            elif object_type is ObjectEnum.RADAR:
                self.__remove_radar(object_id)

        except BaseException as exp:
            print(f'Ошибка при удалении объекта "{object_type.desc}" с id = {object_id}: {exp}')

    @pyqtSlot(float)
    def redraw_radar_beam_path(self, time: float):
        pass

    def __remove_target(self, target_id: int):
        target_path = self.targets[target_id]
        self.__remove_target_path(target_path)
        self.targets.pop(target_id)
        logging.info(f'Цель с id={target_id} удалена')

    def __remove_target_path(self, target_path: TargetPath):
        for vertex in target_path.vertexes:
            self.removeItem(vertex)
        for edge in target_path.edges:
            self.removeItem(edge)

    def __remove_radar(self, radar_id: int):
        self.removeItem(self.radars[radar_id].radar_item)
        self.removeItem(self.radars[radar_id].radar_radius_item)
        self.radars.pop(radar_id)
        logging.info(f'РЛС с id={radar_id} удалена')

    @pyqtSlot(RadarEntity)
    def redraw_radar(self, radar_entity: RadarEntity):
        try:
            if radar_entity.id not in self.radars:
                return

            self.removeItem(self.radars[radar_entity.id].radar_item)
            self.removeItem(self.radars[radar_entity.id].radar_radius_item)

            redraw_radar = RadarObject()
            redraw_radar.radar_item.setPos(
                radar_entity.start_coordinates.to_q_point() -
                QPoint(BASE_SIZE_OBJECT.width() // 2, BASE_SIZE_OBJECT.height() // 2))
            self.addItem(redraw_radar.radar_item)

            redraw_radar.radius = redraw_radar.set_radius(radar_entity.eirp, radar_entity.seff, radar_entity.t_n,
                                                          radar_entity.prf, radar_entity.signal_time,
                                                          radar_entity.n_pulses_proc, radar_entity.operating_freq,
                                                          radar_entity.snr_detection)

            redraw_radar.radius_path.addEllipse(QRectF(redraw_radar.radius,
                                                       redraw_radar.radius,
                                                       2 * redraw_radar.radius,
                                                       2 * redraw_radar.radius))

            redraw_radar.radar_radius_item = self.addPath(redraw_radar.radius_path, QPen(Qt.blue))

            redraw_radar.radar_radius_item.setPos(radar_entity.start_coordinates.to_q_point())
            self.radars[radar_entity.id] = redraw_radar

            self.current_object = None
            self.current_obj_type = None
        except BaseException as exp:
            print(f'{exp}')

    def remove_targets(self):
        for target_id in list(self.targets.keys()):
            self.__remove_target(target_id)
