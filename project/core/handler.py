from PyQt5.QtCore import QObject, pyqtSlot, pyqtSignal

from project import ObjectEnum
from project.core.entities import SarEntity, CoordinatesEntity, TargetEntity

from project.gui import ObjectEditDialog
from project.settings import BASE_SIZE_OBJECT


class Handler(QObject):
    update_sars = pyqtSignal(dict)
    update_targets = pyqtSignal(dict)
    target_deleted = pyqtSignal(int)
    sar_deleted = pyqtSignal(int)
    target_updated = pyqtSignal(object)
    sar_updated = pyqtSignal(object)

    def __init__(self, parent=None):
        super(Handler, self).__init__(parent)
        self.sars = {}
        self.targets = {}
        self.target_id = 0
        self.sar_id = 0

    @pyqtSlot(object)
    def create_sar(self, sar_object: object):
        try:
            coordinates = CoordinatesEntity(
                x=sar_object.x() + BASE_SIZE_OBJECT.width() // 2,
                y=sar_object.y() + BASE_SIZE_OBJECT.height() // 2
            )

            sar_entity = SarEntity(
                id=self.sar_id,
                coordinates=coordinates
            )

            self.sars[self.sar_id] = sar_entity
            self.update_sars.emit(self.sars)
            self.sar_id += 1
            print('РЛС создано')

        except BaseException as exp:
            print(f'Ошибка при создании РЛС: {exp}')

    @pyqtSlot(object)
    def create_target(self, target_object: object):
        try:
            coordinates = CoordinatesEntity(
                x=target_object.x() + BASE_SIZE_OBJECT.width() // 2,
                y=target_object.y() + BASE_SIZE_OBJECT.height() // 2
            )

            target_entity = TargetEntity(
                id=self.target_id,
                coordinates=coordinates
            )

            self.targets[self.target_id] = target_entity
            self.update_targets.emit(self.targets)
            self.target_id += 1
            print('Цель создана')

        except BaseException as exp:
            print(f'Ошибка при создании цели: {exp}')

    @pyqtSlot(int)
    def remove_sar(self, sar_id: int):
        try:
            if sar_id not in self.sars:
                return

            self.sars.pop(sar_id)

            self.sar_deleted.emit(sar_id)
        except BaseException as exp:
            print(f'РЛИ с id = {sar_id} не была удалена: {exp}')

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
    def modify_sar(self, sar_id: int):
        try:
            if sar_id not in self.sars:
                return

            sar_entity = self.sars[sar_id]

            dialog = ObjectEditDialog(object_instance=sar_entity, object_type=ObjectEnum.SAR)
            if dialog.exec() == ObjectEditDialog.Accepted:
                self.sars[sar_id] = dialog.object_instance
            else:
                return

            self.sar_updated.emit(self.sars[sar_id])
        except BaseException as exp:
            print(f'Не удалось изменить РЛИ с id = {sar_id} не удалось изменить: {exp}')

    @pyqtSlot(int)
    def modify_target(self, target_id: int):
        try:
            if target_id not in self.targets:
                return

            target_entity = self.targets[target_id]

            dialog = ObjectEditDialog(object_instance=target_entity, object_type=ObjectEnum.TARGET)
            if dialog.exec() == ObjectEditDialog.Accepted:
                self.targets[target_id] = dialog.object_instance
            else:
                return

            self.target_updated.emit(self.targets[target_id])
        except BaseException as exp:
            print(f'Не удалось изменить цель с id = {target_id} не удалось изменить: {exp}')