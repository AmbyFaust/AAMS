from PyQt5.QtCore import QObject, pyqtSlot, pyqtSignal

from project import ObjectEnum
from project.gui import ObjectEditDialog


class Handler(QObject):
    update_sars = pyqtSignal(dict)
    update_targets = pyqtSignal(dict)
    target_deleted = pyqtSignal(int)
    sar_deleted = pyqtSignal(int)
    target_updated = pyqtSignal(int)
    sar_updated = pyqtSignal(int)

    def __init__(self, parent=None):
        super(Handler, self).__init__(parent)
        self.sars = {}
        self.targets = {}
        self.target_id = 0
        self.sar_id = 0

    @pyqtSlot(object)
    def create_sar(self, sar_object: object):
        try:
            self.sars[self.sar_id] = sar_object
            print(sar_object.x(), sar_object.y())
            self.update_sars.emit(self.sars)
            self.sar_id += 1
            print('РЛС создано')

        except BaseException as exp:
            print(f'Ошибка при создании РЛС: {exp}')

    @pyqtSlot(object)
    def create_target(self, target_object: object):
        try:
            self.targets[self.target_id] = target_object
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

            dialog = ObjectEditDialog(object_instance=None, object_type=ObjectEnum.SAR)
            if dialog.exec() == ObjectEditDialog.Accepted:
                print('SAR dialog')
            else:
                return

            self.sar_updated.emit(sar_id)
        except BaseException as exp:
            print(f'Не удалось изменить РЛИ с id = {sar_id} не удалось изменить: {exp}')

    @pyqtSlot(int)
    def modify_target(self, target_id: int):
        try:
            if target_id not in self.targets:
                return

            dialog = ObjectEditDialog(object_instance=None, object_type=ObjectEnum.TARGET)
            if dialog.exec() == ObjectEditDialog.Accepted:
                print('Target dialog')
            else:
                return

            self.target_updated.emit(target_id)
        except BaseException as exp:
            print(f'Не удалось изменить цель с id = {target_id} не удалось изменить: {exp}')