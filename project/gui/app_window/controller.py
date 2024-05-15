from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot

from project import ObjectEnum
from project.core import RadarEntity, TargetEntity


class Controller(QObject):
    create_radar = pyqtSignal(object)
    create_target = pyqtSignal(object)
    update_radar_list = pyqtSignal(dict)
    update_targets_list = pyqtSignal(dict)
    delete_radar = pyqtSignal(int)
    remove_gui_radar = pyqtSignal(int, object)
    delete_target = pyqtSignal(int)
    remove_gui_target = pyqtSignal(int, object)
    modify_radar = pyqtSignal(int)
    modify_target = pyqtSignal(int)
    redraw_radar = pyqtSignal(object)
    calculate_signal = pyqtSignal()
    modeling_signal = pyqtSignal()

    def __init__(self, parent=None):
        super(Controller, self).__init__(parent)
        self.radars = {}
        self.targets = {}

        self.selected_radar = None
        self.selected_target = None

    def create_object(self, object_type: ObjectEnum, object_instance: object):
        if object_type is ObjectEnum.RADAR:
            self.create_radar.emit(object_instance)
        elif object_type is ObjectEnum.TARGET:
            self.create_target.emit(object_instance)

    @pyqtSlot(dict)
    def update_radar_reviewer(self, radars: dict):
        self.radars = radars.copy()
        self.update_radar_list.emit(self.radars)

    @pyqtSlot(dict)
    def update_targets_reviewer(self, targets: dict):
        self.targets = targets.copy()
        self.update_targets_list.emit(self.targets)

    def is_radar_selected(self, radar_id: int):
        if radar_id in self.radars:
            self.selected_radar = radar_id

    def is_target_selected(self, target_id: int):
        if target_id in self.targets:
            self.selected_target = target_id

    def remove_selected_radar(self):
        if self.selected_radar is None:
            return
        if self.selected_radar not in self.radars:
            return
        self.delete_radar.emit(self.selected_radar)

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

    def update_selected_radar(self):
        if self.selected_radar is None:
            return
        if self.selected_radar not in self.radars:
            return
        self.modify_radar.emit(self.selected_radar)

    @pyqtSlot(int)
    def target_deleted(self, target_id: int):
        try:
            self.targets.pop(target_id)

            self.update_targets_reviewer(self.targets)

            self.remove_gui_target.emit(target_id, ObjectEnum.TARGET)

            self.selected_target = None
        except BaseException as exp:
            print(exp)

    @pyqtSlot(int)
    def radar_deleted(self, radar_id: int):
        try:
            self.radars.pop(radar_id)

            self.update_radar_reviewer(self.radars)

            self.remove_gui_radar.emit(radar_id, ObjectEnum.RADAR)

            self.selected_radar = None
        except BaseException as exp:
            print(exp)

    @pyqtSlot(TargetEntity)
    def target_updated(self, target_entity: TargetEntity):
        try:
            self.targets[target_entity.id] = target_entity

            self.update_targets_reviewer(self.targets)

        except BaseException as exp:
            print(f'Обновление ')

    @pyqtSlot(RadarEntity)
    def radar_updated(self, radar_entity: RadarEntity):
        try:
            self.radars[radar_entity.id] = radar_entity

            self.update_radar_reviewer(self.radars)

            self.redraw_radar.emit(radar_entity)
        except BaseException as exp:
            print(f'Обновление ')
