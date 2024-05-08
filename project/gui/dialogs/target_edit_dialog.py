from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QVBoxLayout, QFormLayout, QLabel, QSpinBox, QComboBox

from project import ObjectEnum, TypeTargetEnum
from project.core import TargetEntity
from . import ObjectEditDialog
from project.settings import BASE_FONT


class TargetEditDialog(ObjectEditDialog):
    def __init__(self, target_instance: TargetEntity, object_type: ObjectEnum, parent=None):
        self.target_instance = target_instance
        super(TargetEditDialog, self).__init__(target_instance, object_type, parent)
        self.__create_widgets()
        self.__create_layouts()

    def __create_widgets(self):
        self.speed_spin_box = QSpinBox()
        self.speed_spin_box.setFont(BASE_FONT)
        self.speed_spin_box.setRange(1, 2000)
        try:
            self.speed_spin_box.setValue(self.target_instance.speed)
        except:
            self.speed_spin_box.setValue(0)

        self.epr_spin_box = QSpinBox()
        self.epr_spin_box.setFont(BASE_FONT)
        self.epr_spin_box.setRange(1, 2000)
        try:
            self.epr_spin_box.setValue(self.target_instance.epr)
        except:
            self.epr_spin_box.setValue(0)

        self.height_spin_box = QSpinBox()
        self.height_spin_box.setFont(BASE_FONT)
        self.height_spin_box.setRange(1, 2000)
        try:
            self.height_spin_box.setValue(self.target_instance.coordinates[0].z)
        except:
            self.height_spin_box.setValue(0)

        self.type_combo_box = QComboBox()
        self.type_combo_box.setFont(BASE_FONT)
        for item in TypeTargetEnum:
            self.type_combo_box.addItem(item.desc, item)
            if item.num == self.target_instance.target_type.num:
                self.type_combo_box.setCurrentIndex(self.type_combo_box.count() - 1)

    def __create_layouts(self):
        common_v_layout = QVBoxLayout()

        common_form_layout = QFormLayout()
        common_form_layout.setLabelAlignment(Qt.AlignLeft)
        common_form_layout.addRow('Скорость, км/ч:', self.speed_spin_box)
        common_form_layout.addRow('ЭПР, м^2:', self.epr_spin_box)
        common_form_layout.addRow('Высота, м:', self.height_spin_box)
        common_form_layout.addRow('Тип:', self.type_combo_box)

        common_v_layout.addLayout(common_form_layout)
        common_v_layout.addWidget(self.button_box)

        self.setLayout(common_v_layout)

    def accept(self):
        try:
            self.target_instance.speed = self.speed_spin_box.value()
            self.target_instance.epr = self.epr_spin_box.value()
            for coordinate in self.target_instance.coordinates:
                coordinate.z = self.height_spin_box.value()
            self.target_instance.target_type = self.type_combo_box.currentData()
        except BaseException as exp:
            print(exp)
        super().accept()
