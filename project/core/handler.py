from PyQt5.QtCore import QObject, pyqtSlot, pyqtSignal

from project import ObjectEnum
from project.core.entities import RadarEntity, CoordinatesEntity, TargetEntity
from project.gui.dialogs import RadarEditDialog

from project.gui.dialogs.target_edit_dialog import TargetEditDialog
from project.gui.objects import TargetPath, RadarObject
from project.settings import BASE_SIZE_OBJECT


class Handler(QObject):
    update_radars = pyqtSignal(dict)
    update_targets = pyqtSignal(dict)
    target_deleted = pyqtSignal(int)
    radar_deleted = pyqtSignal(int)
    target_updated = pyqtSignal(TargetEntity)
    radar_updated = pyqtSignal(RadarEntity)
    remove_from_map = pyqtSignal(object)

    def __init__(self, parent=None):
        super(Handler, self).__init__(parent)
        self.radars = {}
        self.targets = {}
        self.target_id = 0
        self.radar_id = 0

    @pyqtSlot(object)
    def create_radar(self, radar_object: RadarObject):
        try:
            coordinates = CoordinatesEntity(
                x=radar_object.radar_item.x() + BASE_SIZE_OBJECT.width() // 2,
                y=radar_object.radar_item.y() + BASE_SIZE_OBJECT.height() // 2
            )

            radar_entity = RadarEntity(
                id=self.radar_id,
                coordinates=coordinates
            )
            # radar_edit_dialog = RadarEditDialog(radar_instance=radar_entity, object_type=ObjectEnum.RADAR)
            # if radar_edit_dialog.exec() == RadarEditDialog.Accepted:
            self.radars[self.radar_id] = radar_entity
            self.update_radars.emit(self.radars)
            self.radar_id += 1
            print('РЛС создано')
            # else:
            #     self.remove_from_map.emit(radar_object)
            #     print('РЛС не создано')

        except BaseException as exp:
            print(f'Ошибка при создании РЛС: {exp}')

    @pyqtSlot(object)
    def create_target(self, target_object: TargetPath):
        try:
            coordinates = []
            for point in target_object.points:
                coordinates.append(CoordinatesEntity(
                    x=point.x(),
                    y=point.y()
                ))

            target_entity = TargetEntity(
                id=self.target_id,
                coordinates=coordinates
            )
            # target_edit_dialog = TargetEditDialog(target_instance=target_entity, object_type=ObjectEnum.TARGET)
            # if target_edit_dialog.exec() == TargetEditDialog.Accepted:
            self.targets[self.target_id] = target_entity
            self.update_targets.emit(self.targets)
            self.target_id += 1
            print('Цель создана')
            # else:
            #     self.remove_from_map.emit(target_object)
            #     print('Цель не создана')

        except BaseException as exp:
            print(f'Ошибка при создании цели: {exp}')

    @pyqtSlot(int)
    def remove_radar(self, radar_id: int):
        try:
            if radar_id not in self.radars:
                return

            self.radars.pop(radar_id)

            self.radar_deleted.emit(radar_id)
        except BaseException as exp:
            print(f'РЛИ с id = {radar_id} не была удалена: {exp}')

    @pyqtSlot(int)
    def remove_target(self, target_id: int):
        try:
            if target_id not in self.targets:
                return

            self.targets.pop(target_id)

            self.target_deleted.emit(target_id)
        except BaseException as exp:
            print(f'Цель с id = {target_id} не была удалена: {exp}')

    @pyqtSlot(int)
    def modify_radar(self, radar_id: int):
        try:
            if radar_id not in self.radars:
                return

            radar_entity = self.radars[radar_id]

            dialog = RadarEditDialog(radar_instance=radar_entity, object_type=ObjectEnum.RADAR)
            if dialog.exec() == RadarEditDialog.Accepted:
                self.radars[radar_id] = dialog.radar_instance
            else:
                return

            self.radar_updated.emit(self.radars[radar_id])
        except BaseException as exp:
            print(f'Не удалось изменить РЛИ с id = {radar_id} не удалось изменить: {exp}')

    @pyqtSlot(int)
    def modify_target(self, target_id: int):
        try:
            if target_id not in self.targets:
                return

            target_entity = self.targets[target_id]

            dialog = TargetEditDialog(target_instance=target_entity, object_type=ObjectEnum.TARGET)
            if dialog.exec() == TargetEditDialog.Accepted:
                self.targets[target_id] = dialog.target_instance
            else:
                return

            self.target_updated.emit(self.targets[target_id])
        except BaseException as exp:
            print(f'Не удалось изменить цель с id = {target_id} не удалось изменить: {exp}')

    @pyqtSlot()
    def calculate(self):
        print(self.radars)  # смотри radar_entity
        print(self.targets)  # смотри target_entity

