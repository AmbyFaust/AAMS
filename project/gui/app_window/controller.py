from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot

from project import ObjectEnum


class Controller(QObject):
    create_sar = pyqtSignal(object)
    create_target = pyqtSignal(object)
    update_sar_list = pyqtSignal(dict)
    update_targets_list = pyqtSignal(dict)
    delete_sar = pyqtSignal(int)
    remove_gui_sar = pyqtSignal(int, object)
    delete_target = pyqtSignal(int)
    remove_gui_target = pyqtSignal(int, object)
    modify_sar = pyqtSignal(int)
    modify_target = pyqtSignal(int)

    def __init__(self, parent=None):
        super(Controller, self).__init__(parent)
        self.sars = {}
        self.targets = {}

        self.selected_sar = None
        self.selected_target = None

    def create_object(self, object_type: ObjectEnum, object_instance: object):
        if object_type == ObjectEnum.SAR:
            self.create_sar.emit(object_instance)
        elif object_type == ObjectEnum.TARGET:
            self.create_target.emit(object_instance)

    @pyqtSlot(dict)
    def update_sar_reviewer(self, sars: dict):
        self.sars = sars
        self.update_sar_list.emit(sars)

    @pyqtSlot(dict)
    def update_targets_reviewer(self, targets: dict):
        self.targets = targets
        self.update_targets_list.emit(targets)

    def is_sar_selected(self, sar_id: int):
        if sar_id in self.sars:
            self.selected_sar = sar_id

    def is_target_selected(self, target_id: int):
        if target_id in self.targets:
            self.selected_target = target_id

    def remove_selected_sar(self):
        if self.selected_sar is None:
            return
        if self.selected_sar not in self.sars:
            return
        self.delete_sar.emit(self.selected_sar)

    def remove_selected_target(self):
        if self.selected_target is None:
            return
        if self.selected_target not in self.targets:
            return
        self.delete_target.emit(self.selected_target)

    def update_selected_target(self):
        if self.selected_target is None:
            return
        if self.selected_target not in self.targets:
            return
        self.modify_target.emit(self.selected_target)

    def update_selected_sar(self):
        if self.selected_sar is None:
            return
        if self.selected_sar not in self.sars:
            return
        self.modify_sar.emit(self.selected_sar)

    @pyqtSlot(int)
    def target_deleted(self, target_id: int):
        try:
            print(target_id, 'target id')
            self.targets.pop(target_id)

            self.remove_gui_target.emit(target_id, ObjectEnum.TARGET)

            self.selected_target = None
        except BaseException as exp:
            print(f'')

    @pyqtSlot(int)
    def sar_deleted(self, sar_id: int):
        try:
            print(sar_id, 'sar id')
            self.sars.pop(sar_id)

            self.remove_gui_sar.emit(sar_id, ObjectEnum.SAR)

            self.selected_sar = None
        except BaseException as exp:
            print(f'')