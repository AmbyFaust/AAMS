from PyQt5.QtCore import QObject, pyqtSignal, pyqtSlot

from project import ObjectEnum


class Controller(QObject):
    create_rls = pyqtSignal(object)
    update_objects_list = pyqtSignal(dict, dict)

    def create_object(self, object_type: ObjectEnum, object: object):
        if object_type == ObjectEnum.RLS:
            self.create_rls.emit(object)

    @pyqtSlot(dict, dict)
    def update_objects_review(self, target: dict, rls: object):
        self.update_objects_list.emit(target, rls)