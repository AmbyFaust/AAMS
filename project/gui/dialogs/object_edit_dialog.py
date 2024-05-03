from PyQt5.QtWidgets import QDialog, QDialogButtonBox, QLabel, QVBoxLayout, QFormLayout, QLineEdit, QSpinBox
from PyQt5 import QtCore
from PyQt5.QtCore import Qt

from project import ObjectEnum


class ObjectEditDialog(QDialog):
    def __init__(self, object_instance: object, object_type: ObjectEnum, parent=None):
        super(ObjectEditDialog, self).__init__(parent)
        self.setWindowFlags(self.windowFlags() & ~QtCore.Qt.WindowContextHelpButtonHint)
        self.setWindowModality(QtCore.Qt.ApplicationModal)
        self.setFixedWidth(400)

        try:
            self.setWindowTitle(f'Редактирование объекта "{object_type.desc}" c id = {object_instance.id}')
        except:
            self.setWindowTitle('Неизвестный объект')

        self.__create_widgets()

    def __create_widgets(self):
        self.button_box = QDialogButtonBox()
        self.button_box.setStandardButtons(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.button_box.button(QDialogButtonBox.Ok).setText("Принять")
        self.button_box.button(QDialogButtonBox.Cancel).setText("Отмена")
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

    def accept(self):
        super().accept()
