from PyQt5.QtWidgets import QDialog, QDialogButtonBox, QLabel, QVBoxLayout, QFormLayout, QLineEdit, QSpinBox
from PyQt5 import QtCore
from PyQt5.QtCore import Qt

from project import ObjectEnum
from project.settings import BASE_FONT


class ObjectEditDialog(QDialog):
    def __init__(self, parent=None, *, object_instance: object, object_type: ObjectEnum):
        super(ObjectEditDialog, self).__init__(parent)
        self.setWindowFlags(self.windowFlags() & ~QtCore.Qt.WindowContextHelpButtonHint)
        self.setWindowModality(QtCore.Qt.ApplicationModal)
        self.setFixedWidth(400)

        self.object_instance = object_instance

        try:
            self.setWindowTitle(f'Редактирование объекта "{object_type.desc}" c id = {object_instance.id}')
        except:
            self.setWindowTitle('Неизвестный объект')

        self.__create_widgets()
        self.__create_layout()

    def __create_widgets(self):
        self.x_spin_box = QSpinBox()
        self.x_spin_box.setFont(BASE_FONT)
        self.x_spin_box.setRange(0, 1299)
        try:
            self.x_spin_box.setValue(self.object_instance.coordinates.x)
        except:
            self.x_spin_box.setValue(0)

        self.y_spin_box = QSpinBox()
        self.y_spin_box.setFont(BASE_FONT)
        self.y_spin_box.setRange(0, 899)
        try:
            self.y_spin_box.setValue(self.object_instance.coordinates.y)
        except:
            self.y_spin_box.setValue(0)

        self.button_box = QDialogButtonBox()
        self.button_box.setStandardButtons(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.button_box.button(QDialogButtonBox.Ok).setText("Принять")
        self.button_box.button(QDialogButtonBox.Cancel).setText("Отмена")
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

    def __create_layout(self):
        common_v_layout = QVBoxLayout()

        common_form_layout = QFormLayout()
        common_form_layout.setLabelAlignment(Qt.AlignLeft)
        common_form_layout.addRow('X:', self.x_spin_box)
        common_form_layout.addRow('Y:', self.y_spin_box)

        common_v_layout.addLayout(common_form_layout)
        common_v_layout.addWidget(QLabel())
        common_v_layout.addWidget(self.button_box)

        self.setLayout(common_v_layout)

    def accept(self):
        try:
            self.object_instance.coordinates.x = self.x_spin_box.value()
            self.object_instance.coordinates.y = self.y_spin_box.value()
        except BaseException as exp:
            print(exp)
        super().accept()
