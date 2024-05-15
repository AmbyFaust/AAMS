import os
import typing

from PyQt5 import QtCore
from PyQt5.QtWidgets import QDialog, QLineEdit, QPushButton, QDialogButtonBox, QHBoxLayout, QLabel, QVBoxLayout

from project import settings
from project.gui.dialogs.open_dialog import QOpenFilesDialog
from project.settings import BASE_FONT


class ChoosingModelingFileDialog(QDialog):
    def __init__(self, parent=None):
        super(ChoosingModelingFileDialog, self).__init__(parent)
        self.setWindowFlags(self.windowFlags() & ~QtCore.Qt.WindowContextHelpButtonHint)
        self.setWindowModality(QtCore.Qt.ApplicationModal)
        self.setWindowTitle('Настройки AAMS')
        self.setMinimumWidth(600)
        self.__create_widgets()
        self.__create_layout()

    def __create_widgets(self):
        self.input_file_path_lineedit = QLineEdit()
        self.input_file_path_lineedit.setReadOnly(True)
        self.input_file_path_lineedit.setText(str(settings.OUTPUT_FILE_PATH))
        self.input_file_path_lineedit.setFont(BASE_FONT)

        self.input_file_button = QPushButton('...')
        self.input_file_button.clicked.connect(self.__input_file_button_clicked)

        self.button_box = QDialogButtonBox()
        self.button_box.setStandardButtons(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        self.button_box.button(QDialogButtonBox.Ok).setText("Принять")
        self.button_box.button(QDialogButtonBox.Cancel).setText("Отмена")
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

    def __create_layout(self):
        main_v_layout = QVBoxLayout()

        input_file_layout = QHBoxLayout()
        input_file_layout.addWidget(QLabel('Директория входного файла: '))
        input_file_layout.addWidget(self.input_file_path_lineedit)
        input_file_layout.addWidget(self.input_file_button)

        main_v_layout.addLayout(input_file_layout)
        main_v_layout.addWidget(self.button_box)

        self.setLayout(main_v_layout)

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

    def accept(self):
        settings.OUTPUT_FILE_PATH = self.input_file_path_lineedit.text()
        super(ChoosingModelingFileDialog, self).accept()
