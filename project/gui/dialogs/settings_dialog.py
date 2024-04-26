import os.path
import typing

from PyQt5.QtWidgets import QDialog, QLineEdit, QPushButton, QHBoxLayout, QLabel, QVBoxLayout, QSpinBox, \
    QDialogButtonBox
from PyQt5 import QtCore

from project import settings
from project.gui.dialogs.open_dialog import QOpenFilesDialog
from project.settings import BASE_FONT


class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super(SettingsDialog, self).__init__(parent)
        self.setWindowFlags(self.windowFlags() & ~QtCore.Qt.WindowContextHelpButtonHint)
        self.setWindowModality(QtCore.Qt.ApplicationModal)
        self.setWindowTitle('Настройки AAMS')
        self.setMinimumWidth(600)
        self.__create_widgets()
        self.__create_layout()
        self.__setup_connections()

    def __create_widgets(self):
        self.input_file_path_lineedit = QLineEdit()
        self.input_file_path_lineedit.setReadOnly(True)
        self.input_file_path_lineedit.setText(str(settings.INPUT_FILE_PATH))
        self.input_file_path_lineedit.setFont(BASE_FONT)

        self.input_file_button = QPushButton('...')

        self.sar_radius_spinbox = QSpinBox()
        self.sar_radius_spinbox.setFont(BASE_FONT)
        self.sar_radius_spinbox.setRange(0, 200)
        self.sar_radius_spinbox.setValue(settings.SAR_RADIUS)

        self.button_box = QDialogButtonBox()
        self.button_box.setStandardButtons(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.button_box.button(QDialogButtonBox.Ok).setText("Принять")
        self.button_box.button(QDialogButtonBox.Cancel).setText("Отмена")
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

    def __create_layout(self):
        input_file_layout = QHBoxLayout()
        input_file_layout.addWidget(QLabel('Директория входного файла: '))
        input_file_layout.addWidget(self.input_file_path_lineedit)
        input_file_layout.addWidget(self.input_file_button)

        sar_radius_layout = QHBoxLayout()
        sar_radius_layout.addWidget(QLabel('Радиус действия РЛС: '))
        sar_radius_layout.addWidget(self.sar_radius_spinbox)

        main_v_layout = QVBoxLayout()
        main_v_layout.addLayout(input_file_layout)
        main_v_layout.addWidget(QLabel(''))
        main_v_layout.addLayout(sar_radius_layout)
        main_v_layout.addWidget(QLabel(''))
        main_v_layout.addWidget(self.button_box)

        self.setLayout(main_v_layout)

    def __setup_connections(self):
        self.input_file_button.clicked.connect(self.__input_file_button_clicked)

    def accept(self):
        settings.INPUT_FILE_PATH = self.input_file_path_lineedit.text()
        settings.SAR_RADIUS = self.sar_radius_spinbox.value()
        super(SettingsDialog, self).accept()

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
