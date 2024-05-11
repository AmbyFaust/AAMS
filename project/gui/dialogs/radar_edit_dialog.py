from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QVBoxLayout, QFormLayout, QLabel, QSpinBox, QDoubleSpinBox

from project import ObjectEnum
from project.core import RadarEntity
from . import ObjectEditDialog
from project.settings import (BASE_FONT, EIRP, SEFF, BW_U, BW_V, T_N, PRF, N_PULSES_PROC,
                              OPERATING_FREQ, START_TIME, SNR_DETECTION)


class RadarEditDialog(ObjectEditDialog):
    def __init__(self, radar_instance: RadarEntity, object_type: ObjectEnum, parent=None):
        self.radar_instance = radar_instance
        super(RadarEditDialog, self).__init__(radar_instance, object_type, parent)
        self.__create_widgets()
        self.__create_layouts()

    def __create_widgets(self):
        self.x_spin_box = QSpinBox()
        self.x_spin_box.setFont(BASE_FONT)
        self.x_spin_box.setRange(0, 1299)
        try:
            self.x_spin_box.setValue(int(self.radar_instance.start_coordinates.x))
        except:
            self.x_spin_box.setValue(0)

        self.y_spin_box = QSpinBox()
        self.y_spin_box.setFont(BASE_FONT)
        self.y_spin_box.setRange(0, 899)
        try:
            self.y_spin_box.setValue(int(self.radar_instance.start_coordinates.y))
        except:
            self.y_spin_box.setValue(0)

        self.eirp_spinbox = QSpinBox()
        self.eirp_spinbox.setFont(BASE_FONT)
        self.eirp_spinbox.setRange(0, 10000)
        self.eirp_spinbox.setValue(EIRP)

        self.seff_spinbox = QSpinBox()
        self.seff_spinbox.setFont(BASE_FONT)
        self.seff_spinbox.setRange(0, 10000)
        self.seff_spinbox.setValue(SEFF)

        self.bw_u_spinbox = QSpinBox()
        self.bw_u_spinbox.setFont(BASE_FONT)
        self.bw_u_spinbox.setRange(1, 44)
        self.bw_u_spinbox.setValue(BW_U)

        self.bw_v_spinbox = QSpinBox()
        self.bw_v_spinbox.setFont(BASE_FONT)
        self.bw_v_spinbox.setRange(1, 44)
        self.bw_v_spinbox.setValue(BW_V)

        self.scanning_v = QLabel()

        self.t_n_spinbox = QSpinBox()
        self.t_n_spinbox.setFont(BASE_FONT)
        self.t_n_spinbox.setRange(273, 400)
        self.t_n_spinbox.setValue(T_N)

        self.prf_spinbox = QDoubleSpinBox()
        self.prf_spinbox.setFont(BASE_FONT)
        self.prf_spinbox.setRange(0.0001, 10000)
        self.prf_spinbox.setValue(PRF)

        self.n_pulses_proc_spinbox = QSpinBox()
        self.n_pulses_proc_spinbox.setFont(BASE_FONT)
        self.n_pulses_proc_spinbox.setRange(0, 1000)
        self.n_pulses_proc_spinbox.setValue(N_PULSES_PROC)

        self.operating_freq_spinbox = QSpinBox()
        self.operating_freq_spinbox.setFont(BASE_FONT)
        self.operating_freq_spinbox.setRange(0, 1000)
        self.operating_freq_spinbox.setValue(OPERATING_FREQ)

        self.start_time_spinbox = QSpinBox()
        self.start_time_spinbox.setFont(BASE_FONT)
        self.start_time_spinbox.setRange(0, 10)
        self.start_time_spinbox.setValue(START_TIME)

        self.snr_detection_spinbox = QSpinBox()
        self.snr_detection_spinbox.setFont(BASE_FONT)
        self.snr_detection_spinbox.setRange(1, 100)
        self.snr_detection_spinbox.setValue(SNR_DETECTION)

    def __create_layouts(self):
        common_v_layout = QVBoxLayout()

        common_form_layout = QFormLayout()
        common_form_layout.setLabelAlignment(Qt.AlignLeft)
        common_form_layout.addRow('X, м:', self.x_spin_box)
        common_form_layout.addRow('Y, м:', self.y_spin_box)
        common_form_layout.addRow('Эффективная изотропная излучаемая мощность:', self.eirp_spinbox)
        common_form_layout.addRow('Эффективная площадь антенны:', self.seff_spinbox)
        common_form_layout.addRow('Ширина луча по азимуту, град:', self.bw_u_spinbox)
        common_form_layout.addRow('Ширина луча по углу места, град:', self.bw_v_spinbox)
        common_form_layout.addRow('Пределы сканирования по углу места:', self.scanning_v)
        common_form_layout.addRow('Шумовая температура, К:', self.t_n_spinbox)
        common_form_layout.addRow('Частота повторения импульсов:', self.prf_spinbox)
        common_form_layout.addRow('Количество импульсов в пачке:', self.n_pulses_proc_spinbox)
        common_form_layout.addRow('Рабочая частота:', self.operating_freq_spinbox)
        common_form_layout.addRow('Начальное время:', self.start_time_spinbox)
        common_form_layout.addRow('ОСШ для обнаружения:', self.snr_detection_spinbox)

        common_v_layout.addLayout(common_form_layout)
        common_v_layout.addWidget(self.button_box)
        self.setLayout(common_v_layout)

    def accept(self):
        try:
            self.radar_instance.start_coordinates.x = int(self.x_spin_box.value())
            self.radar_instance.start_coordinates.y = int(self.y_spin_box.value())
            self.radar_instance.eirp = int(self.eirp_spinbox.value())
            self.radar_instance.seff = int(self.seff_spinbox.value())
            self.radar_instance.bw_u = int(self.bw_u_spinbox.value())
            self.radar_instance.bw_v = int(self.bw_v_spinbox.value())
            # self.radar_instance.scanning_v = ''
            self.radar_instance.t_n = int(self.t_n_spinbox.value())
            self.radar_instance.prf = int(self.prf_spinbox.value())
            self.radar_instance.n_pulses_proc = int(self.n_pulses_proc_spinbox.value())
            self.radar_instance.operating_freq = int(self.operating_freq_spinbox.value())
            self.radar_instance.start_time = int(self.start_time_spinbox.value())
            self.radar_instance.snr_detection = int(self.snr_detection_spinbox.value())
        except BaseException as exp:
            print(exp)
        super().accept()
