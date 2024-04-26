from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QVBoxLayout, QFormLayout, QLabel, QSpinBox

from project import ObjectEnum
from project.core import SarEntity
from . import ObjectEditDialog
from project.settings import BASE_FONT


class SarEditDialog(ObjectEditDialog):
    def __init__(self, sar_instance: SarEntity, object_type: ObjectEnum, parent=None):
        self.sar_instance = sar_instance
        super(SarEditDialog, self).__init__(sar_instance, object_type, parent)
        self.__create_widgets()
        self.__create_layouts()

    def __create_widgets(self):
        self.x_spin_box = QSpinBox()
        self.x_spin_box.setFont(BASE_FONT)
        self.x_spin_box.setRange(0, 1299)
        try:
            self.x_spin_box.setValue(int(self.sar_instance.coordinates.x))
        except:
            self.x_spin_box.setValue(0)

        self.y_spin_box = QSpinBox()
        self.y_spin_box.setFont(BASE_FONT)
        self.y_spin_box.setRange(0, 899)
        try:
            self.y_spin_box.setValue(int(self.sar_instance.coordinates.y))
        except:
            self.y_spin_box.setValue(0)

    def __create_layouts(self):
        common_v_layout = QVBoxLayout()

        common_form_layout = QFormLayout()
        common_form_layout.setLabelAlignment(Qt.AlignLeft)
        common_form_layout.addRow('X, м:', self.x_spin_box)
        common_form_layout.addRow('Y, м:', self.y_spin_box)

        common_v_layout.addLayout(common_form_layout)
        common_v_layout.addWidget(self.button_box)
        self.setLayout(common_v_layout)

    def accept(self):
        try:
            self.sar_instance.coordinates.x = int(self.x_spin_box.value())
            self.sar_instance.coordinates.y = int(self.y_spin_box.value())
        except BaseException as exp:
            print(exp)
        super().accept()
