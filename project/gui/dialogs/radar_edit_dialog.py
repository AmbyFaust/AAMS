from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QVBoxLayout, QFormLayout, QLabel, QSpinBox, QDoubleSpinBox, QHBoxLayout

from project import ObjectEnum, settings
from project.core import RadarEntity
from . import ObjectEditDialog

class RadarEditDialog(ObjectEditDialog):
    def __init__(self, radar_instance: RadarEntity, object_type: ObjectEnum, parent=None):
        self.radar_instance = radar_instance
        super(RadarEditDialog, self).__init__(radar_instance, object_type, parent)
        self.__create_widgets()
        self.__create_layouts()

    def __create_widgets(self):
        self.x_spin_box = QSpinBox()
        self.x_spin_box.setFont(settings.BASE_FONT)
        self.x_spin_box.setRange(0, 1299)
        try:
            self.x_spin_box.setValue(int(self.radar_instance.start_coordinates.x))
        except:
            self.x_spin_box.setValue(0)

        self.y_spin_box = QSpinBox()
        self.y_spin_box.setFont(settings.BASE_FONT)
        self.y_spin_box.setRange(0, 899)
        try:
            self.y_spin_box.setValue(int(self.radar_instance.start_coordinates.y))
        except:
            self.y_spin_box.setValue(0)

        self.eirp_spinbox = QSpinBox()
        self.eirp_spinbox.setFont(settings.BASE_FONT)
        self.eirp_spinbox.setRange(0, 10**7)
        self.eirp_spinbox.setValue(settings.EIRP)

        self.seff_spinbox = QSpinBox()
        self.seff_spinbox.setFont(settings.BASE_FONT)
        self.seff_spinbox.setRange(0, 100)
        self.seff_spinbox.setValue(settings.SEFF)

        self.bw_u_spinbox = QSpinBox()
        self.bw_u_spinbox.setFont(settings.BASE_FONT)
        self.bw_u_spinbox.setRange(1, 44)
        self.bw_u_spinbox.setValue(settings.BW_U)

        self.bw_v_spinbox = QSpinBox()
        self.bw_v_spinbox.setFont(settings.BASE_FONT)
        self.bw_v_spinbox.setRange(1, 44)
        self.bw_v_spinbox.setValue(settings.BW_V)

        self.scanning_v_min_label = QLabel('От:')

        self.scanning_v_min = QSpinBox()
        self.scanning_v_min.setFont(settings.BASE_FONT)
        self.scanning_v_min.setRange(1, 359)
        self.scanning_v_min.setValue(settings.SCANNING_V[0])

        self.scanning_v_max_label = QLabel('До:')

        self.scanning_v_max = QSpinBox()
        self.scanning_v_max.setFont(settings.BASE_FONT)
        self.scanning_v_max.setRange(2, 360)
        self.scanning_v_max.setValue(settings.SCANNING_V[1])

        self.t_n_spinbox = QSpinBox()
        self.t_n_spinbox.setFont(settings.BASE_FONT)
        self.t_n_spinbox.setRange(273, 10000)
        self.t_n_spinbox.setValue(settings.T_N)

        self.prf_spinbox = QDoubleSpinBox()
        self.prf_spinbox.setFont(settings.BASE_FONT)
        self.prf_spinbox.setRange(0.0001, 10**7)
        self.prf_spinbox.setValue(settings.PRF)

        self.signal_time_spinbox = QDoubleSpinBox()
        self.signal_time_spinbox.setFont(settings.BASE_FONT)
        self.signal_time_spinbox.setRange(10**(-8), 1)
        self.signal_time_spinbox.setValue(settings.SIGNAL_TIME)

        self.n_pulses_proc_spinbox = QSpinBox()
        self.n_pulses_proc_spinbox.setFont(settings.BASE_FONT)
        self.n_pulses_proc_spinbox.setRange(1, 10000)
        self.n_pulses_proc_spinbox.setValue(settings.N_PULSES_PROC)

        self.operating_freq_spinbox = QDoubleSpinBox()
        self.operating_freq_spinbox.setFont(settings.BASE_FONT)
        self.operating_freq_spinbox.setRange(15*10**5, 15*10**10)
        self.operating_freq_spinbox.setValue(settings.OPERATING_FREQ)

        self.start_time_spinbox = QSpinBox()
        self.start_time_spinbox.setFont(settings.BASE_FONT)
        self.start_time_spinbox.setRange(0, 10)
        self.start_time_spinbox.setValue(settings.START_TIME)

        self.snr_detection_spinbox = QSpinBox()
        self.snr_detection_spinbox.setFont(settings.BASE_FONT)
        self.snr_detection_spinbox.setRange(1, 100)
        self.snr_detection_spinbox.setValue(settings.SNR_DETECTION)

        self.scanning_v_min.valueChanged.connect(self.__validate_values)
        self.scanning_v_max.valueChanged.connect(self.__validate_values)

    def __create_layouts(self):
        common_v_layout = QVBoxLayout()

        scanning_v_h_layout = QHBoxLayout()
        scanning_v_h_layout.addWidget(self.scanning_v_min_label)
        scanning_v_h_layout.addWidget(self.scanning_v_min)
        scanning_v_h_layout.addWidget(self.scanning_v_max_label)
        scanning_v_h_layout.addWidget(self.scanning_v_max)

        common_form_layout = QFormLayout()
        common_form_layout.setLabelAlignment(Qt.AlignLeft)
        common_form_layout.addRow('X, м:', self.x_spin_box)
        common_form_layout.addRow('Y, м:', self.y_spin_box)
        common_form_layout.addRow('Эффективная изотропная излучаемая мощность:', self.eirp_spinbox)
        common_form_layout.addRow('Эффективная площадь антенны:', self.seff_spinbox)
        common_form_layout.addRow('Ширина луча по азимуту, град:', self.bw_u_spinbox)
        common_form_layout.addRow('Ширина луча по углу места, град:', self.bw_v_spinbox)
        common_form_layout.addRow('Пределы сканирования по углу места:', scanning_v_h_layout)
        common_form_layout.addRow('Шумовая температура, К:', self.t_n_spinbox)
        common_form_layout.addRow('Частота повторения импульсов:', self.prf_spinbox)
        common_form_layout.addRow('Время сигнала:', self.signal_time_spinbox)
        common_form_layout.addRow('Количество импульсов в пачке:', self.n_pulses_proc_spinbox)
        common_form_layout.addRow('Рабочая частота:', self.operating_freq_spinbox)
        common_form_layout.addRow('Начальное время:', self.start_time_spinbox)
        common_form_layout.addRow('ОСШ для обнаружения:', self.snr_detection_spinbox)

        common_v_layout.addLayout(common_form_layout)
        common_v_layout.addWidget(self.button_box)
        self.setLayout(common_v_layout)

    def __validate_values(self):
        min_value = self.scanning_v_min.value()
        max_value = self.scanning_v_max.value()
        if min_value >= max_value:
            self.scanning_v_max.setValue(min_value + 1)

    def accept(self):
        try:
            self.radar_instance.start_coordinates.x = int(self.x_spin_box.value())
            self.radar_instance.start_coordinates.y = int(self.y_spin_box.value())
            self.radar_instance.eirp = int(self.eirp_spinbox.value())
            self.radar_instance.seff = int(self.seff_spinbox.value())
            self.radar_instance.bw_u = int(self.bw_u_spinbox.value())
            self.radar_instance.bw_v = int(self.bw_v_spinbox.value())
            self.radar_instance.scanning_v = [int(self.scanning_v_min.value()), int(self.scanning_v_max.value())]
            self.radar_instance.t_n = int(self.t_n_spinbox.value())
            self.radar_instance.prf = int(self.prf_spinbox.value())
            self.radar_instance.signal_time = int(self.signal_time_spinbox.value())
            self.radar_instance.n_pulses_proc = int(self.n_pulses_proc_spinbox.value())
            self.radar_instance.operating_freq = int(self.operating_freq_spinbox.value())
            self.radar_instance.start_time = int(self.start_time_spinbox.value())
            self.radar_instance.snr_detection = int(self.snr_detection_spinbox.value())
        except BaseException as exp:
            print(exp)
        super().accept()
