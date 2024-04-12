from PyQt5.QtCore import QObject, pyqtSignal

from project.gui.enums import ObjectEnum


class Controller(QObject):
    create_rls = pyqtSignal()

    def create_object(self, object_type: ObjectEnum):
        if object_type == ObjectEnum.RLS:
            self.create_rls.emit()