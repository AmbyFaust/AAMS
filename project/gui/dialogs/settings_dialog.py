import os.path
import typing

from PyQt5.QtWidgets import QDialog, QLineEdit, QPushButton, QHBoxLayout, QLabel, QVBoxLayout, QSpinBox, \
    QDialogButtonBox, QWidget, QDoubleSpinBox, QFormLayout, QComboBox, QTabWidget
from PyQt5 import QtCore

from project import TypeTargetEnum
from project import settings
from project.gui.dialogs.open_dialog import QOpenFilesDialog
from project.settings import BASE_FONT, SIGNAL_TIME, SCANNING_V


class RadarSettings(QWidget):
    def __init__(self, parent=None):
        super(RadarSettings, self).__init__(parent)
        self.__create_widgets()
        self.__create_layout()

    def __create_widgets(self):
        self.eirp_spinbox = QSpinBox()
        self.eirp_spinbox.setFont(BASE_FONT)
        self.eirp_spinbox.setRange(0, 10000)
        self.eirp_spinbox.setValue(settings.EIRP)

        self.seff_spinbox = QSpinBox()
        self.seff_spinbox.setFont(BASE_FONT)
        self.seff_spinbox.setRange(0, 10000)
        self.seff_spinbox.setValue(settings.SEFF)

        self.bw_u_spinbox = QSpinBox()
        self.bw_u_spinbox.setFont(BASE_FONT)
        self.bw_u_spinbox.setRange(1, 44)
        self.bw_u_spinbox.setValue(settings.BW_U)

        self.bw_v_spinbox = QSpinBox()
        self.bw_v_spinbox.setFont(BASE_FONT)
        self.bw_v_spinbox.setRange(1, 44)
        self.bw_v_spinbox.setValue(settings.BW_V)

        self.scanning_v_min_label = QLabel('От:')

        self.scanning_v_min = QSpinBox()
        self.scanning_v_min.setFont(BASE_FONT)
        self.scanning_v_min.setRange(1, 43)
        self.scanning_v_min.setValue(SCANNING_V[0])

        self.scanning_v_max_label = QLabel('До:')

        self.scanning_v_max = QSpinBox()
        self.scanning_v_max.setFont(BASE_FONT)
        self.scanning_v_max.setRange(2, 44)
        self.scanning_v_max.setValue(SCANNING_V[1])

        self.t_n_spinbox = QSpinBox()
        self.t_n_spinbox.setFont(BASE_FONT)
        self.t_n_spinbox.setRange(273, 400)
        self.t_n_spinbox.setValue(settings.T_N)

        self.prf_spinbox = QDoubleSpinBox()
        self.prf_spinbox.setFont(BASE_FONT)
        self.prf_spinbox.setRange(0.0001, 10000)
        self.prf_spinbox.setValue(settings.PRF)

        self.signal_time_spinbox = QDoubleSpinBox()
        self.signal_time_spinbox.setFont(BASE_FONT)
        self.signal_time_spinbox.setRange(1, 100)
        self.signal_time_spinbox.setValue(SIGNAL_TIME)

        self.n_pulses_proc_spinbox = QSpinBox()
        self.n_pulses_proc_spinbox.setFont(BASE_FONT)
        self.n_pulses_proc_spinbox.setRange(0, 1000)
        self.n_pulses_proc_spinbox.setValue(settings.N_PULSES_PROC)

        self.operating_freq_spinbox = QSpinBox()
        self.operating_freq_spinbox.setFont(BASE_FONT)
        self.operating_freq_spinbox.setRange(0, 1000)
        self.operating_freq_spinbox.setValue(settings.OPERATING_FREQ)

        self.start_time_spinbox = QSpinBox()
        self.start_time_spinbox.setFont(BASE_FONT)
        self.start_time_spinbox.setRange(0, 10)
        self.start_time_spinbox.setValue(settings.START_TIME)

        self.snr_detection_spinbox = QSpinBox()
        self.snr_detection_spinbox.setFont(BASE_FONT)
        self.snr_detection_spinbox.setRange(1, 100)
        self.snr_detection_spinbox.setValue(settings.SNR_DETECTION)

        self.scanning_v_min.valueChanged.connect(self.__validate_values)
        self.scanning_v_max.valueChanged.connect(self.__validate_values)

    def __create_layout(self):
        scanning_v_h_layout = QHBoxLayout()
        scanning_v_h_layout.addWidget(self.scanning_v_min_label)
        scanning_v_h_layout.addWidget(self.scanning_v_min)
        scanning_v_h_layout.addWidget(self.scanning_v_max_label)
        scanning_v_h_layout.addWidget(self.scanning_v_max)

        common_form_layout = QFormLayout()
        common_form_layout.addRow('Эффективная изотропная излучаемая мощность:', self.eirp_spinbox)
        common_form_layout.addRow('Эффективная площадь антенны:', self.seff_spinbox)
        common_form_layout.addRow('Ширина луча по азимуту, град:', self.bw_u_spinbox)
        common_form_layout.addRow('Ширина луча по углу места, град:', self.bw_v_spinbox)
        common_form_layout.addRow('Шумовая температура, К:', self.t_n_spinbox)
        common_form_layout.addRow('Частота повторения импульсов:', self.prf_spinbox)
        common_form_layout.addRow('Пределы сканирования по углу места:', scanning_v_h_layout)
        common_form_layout.addRow('Время сигнала:', self.signal_time_spinbox)
        common_form_layout.addRow('Количество импульсов в пачке:', self.n_pulses_proc_spinbox)
        common_form_layout.addRow('Рабочая частота:', self.operating_freq_spinbox)
        common_form_layout.addRow('Начальное время:', self.start_time_spinbox)
        common_form_layout.addRow('ОСШ для обнаружения:', self.snr_detection_spinbox)

        self.setLayout(common_form_layout)

    def __validate_values(self):
        min_value = self.scanning_v_min.value()
        max_value = self.scanning_v_max.value()
        if min_value >= max_value:
            self.scanning_v_max.setValue(min_value + 1)


class TargetSettings(QWidget):
    def __init__(self, parent=None):
        super(TargetSettings, self).__init__(parent)
        self.__create_widgets()
        self.__create_layout()

    def __create_widgets(self):
        self.speed_spinbox = QSpinBox()
        self.speed_spinbox.setFont(BASE_FONT)
        self.speed_spinbox.setRange(1, 1000)
        self.speed_spinbox.setValue(settings.SPEED)

        self.target_type_combobox = QComboBox()
        self.target_type_combobox.setFont(BASE_FONT)
        self.target_type_combobox.addItem(TypeTargetEnum.first.desc)
        self.target_type_combobox.addItem(TypeTargetEnum.second.desc)
        self.target_type_combobox.setCurrentText(settings.TARGET_TYPE.desc)

        self.epr_spinbox = QSpinBox()
        self.epr_spinbox.setFont(BASE_FONT)
        self.epr_spinbox.setRange(1, 1000)
        self.epr_spinbox.setValue(settings.EPR)

        self.height_spinbox = QSpinBox()
        self.height_spinbox.setFont(BASE_FONT)
        self.height_spinbox.setRange(1, 1000)
        self.height_spinbox.setValue(settings.HEIGHT)

    def __create_layout(self):
        common_form_layout = QFormLayout()
        common_form_layout.addRow('Скорость цели:', self.speed_spinbox)
        common_form_layout.addRow('Тип цели:', self.target_type_combobox)
        common_form_layout.addRow('ЭПР:', self.epr_spinbox)
        common_form_layout.addRow('Высота цели:', self.height_spinbox)

        self.setLayout(common_form_layout)


class MainSettings(QWidget):
    def __init__(self, parent=None):
        super(MainSettings, self).__init__(parent)
        self.__create_widgets()
        self.__create_layout()

    def __create_widgets(self):
        self.input_file_path_lineedit = QLineEdit()
        self.input_file_path_lineedit.setReadOnly(True)
        self.input_file_path_lineedit.setText(str(settings.INPUT_FILE_PATH))
        self.input_file_path_lineedit.setFont(BASE_FONT)

        self.input_file_button = QPushButton('...')
        self.input_file_button.clicked.connect(self.__input_file_button_clicked)

    def __create_layout(self):
        input_file_layout = QHBoxLayout()
        input_file_layout.addWidget(QLabel('Директория входного файла: '))
        input_file_layout.addWidget(self.input_file_path_lineedit)
        input_file_layout.addWidget(self.input_file_button)

        self.setLayout(input_file_layout)

    def __input_file_button_clicked(self):
        folder_path = self.__select_folder('Выбрать директорию входного файла')
        if folder_path is None:
            return
        try:
            if not os.path.exists(folder_path):
                return
            self.input_file_path_lineedit.setText(folder_path)
        except BaseException as exp:
            print(exp)

    @staticmethod
    def __select_folder(window_title: str = 'Выбрать директорию') -> typing.Union[str, None]:
        file_dialog = QOpenFilesDialog()
        file_dialog.setWindowTitle(window_title)
        file_dialog.setOption(QOpenFilesDialog.ShowDirsOnly)
        file_dialog.setFileMode(QOpenFilesDialog.Directory)
        file_dialog.setDirectory('.')
        if file_dialog.exec() != QOpenFilesDialog.Accepted:
            return None
        if len(file_dialog.selectedFiles()) > 0:
            return file_dialog.selectedFiles()[0]

        return None


class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super(SettingsDialog, self).__init__(parent)
        self.setWindowFlags(self.windowFlags() & ~QtCore.Qt.WindowContextHelpButtonHint)
        self.setWindowModality(QtCore.Qt.ApplicationModal)
        self.setWindowTitle('Настройки AAMS')
        self.setMinimumWidth(600)
        self.__create_widgets()
        self.__create_layout()

    def __create_widgets(self):
        self.main_widget = QTabWidget()

        self.main_settings = MainSettings()
        self.radar_settings = RadarSettings()
        self.target_settings = TargetSettings()

        self.main_widget.addTab(self.main_settings, 'Основные')
        self.main_widget.addTab(self.radar_settings, 'Радар')
        self.main_widget.addTab(self.target_settings, 'Цель')
        self.main_widget.setCurrentWidget(self.main_settings)

        self.button_box = QDialogButtonBox()
        self.button_box.setStandardButtons(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.button_box.button(QDialogButtonBox.Ok).setText("Принять")
        self.button_box.button(QDialogButtonBox.Cancel).setText("Отмена")
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

    def __create_layout(self):
        main_v_layout = QVBoxLayout()
        main_v_layout.addWidget(self.main_widget)
        main_v_layout.addWidget(QLabel(''))
        main_v_layout.addWidget(self.button_box)

        self.setLayout(main_v_layout)

    def accept(self):
        settings.INPUT_FILE_PATH = self.main_settings.input_file_path_lineedit.text()
        settings.EIRP = self.radar_settings.eirp_spinbox.value()
        settings.SEFF = self.radar_settings.seff_spinbox.value()
        settings.BW_U = self.radar_settings.bw_u_spinbox.value()
        settings.BW_V = self.radar_settings.bw_v_spinbox.value()
        settings.T_N = self.radar_settings.t_n_spinbox.value()
        settings.PRF = self.radar_settings.prf_spinbox.value()
        settings.SCANNING_V = [self.radar_settings.scanning_v_min.value(), self.radar_settings.scanning_v_max.value()]
        settings.SIGNAL_TIME = self.radar_settings.start_time_spinbox.value()
        settings.N_PULSES_PROC = self.radar_settings.n_pulses_proc_spinbox.value()
        settings.OPERATING_FREQ = self.radar_settings.operating_freq_spinbox.value()
        settings.START_TIME = self.radar_settings.start_time_spinbox.value()
        settings.SNR_DETECTION = self.radar_settings.snr_detection_spinbox.value()

        settings.SPEED = self.target_settings.speed_spinbox.value()
        settings.TARGET_TYPE = TypeTargetEnum.get_target_type_from_desc(
            self.target_settings.target_type_combobox.currentText())
        settings.EPR = self.target_settings.epr_spinbox.value()
        settings.HEIGHT = self.target_settings.height_spinbox.value()
        super(SettingsDialog, self).accept()