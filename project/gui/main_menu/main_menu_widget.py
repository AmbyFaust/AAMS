from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QCloseEvent
from PyQt5.QtWidgets import QPushButton, QVBoxLayout, QLabel, QApplication

from project.gui.base_form_classes import QWidgetBase
from project.gui.common import BUTTON_FONT


class MainMenuWidget(QWidgetBase):
    start_app = pyqtSignal()
    set_settings = pyqtSignal()
    exit_app = pyqtSignal()

    def __init__(self, parent=None):
        super(MainMenuWidget, self).__init__(parent)
        self.__create_widgets()
        self.__create_layout()

        self.setWindowTitle('AAMS')
        self.setFixedWidth(400)
        self.setFixedHeight(400)

    def __create_widgets(self):
        self.start_app_button = QPushButton('Запуск')
        self.start_app_button.setFont(BUTTON_FONT)
        self.start_app_button.clicked.connect(lambda *_: self.start_app.emit())

        self.set_settings_button = QPushButton('Настройки')
        self.set_settings_button.setFont(BUTTON_FONT)
        self.set_settings_button.clicked.connect(lambda *_: self.set_settings.emit())

        self.exit_app_button = QPushButton('Выход')
        self.exit_app_button.setFont(BUTTON_FONT)
        self.exit_app_button.clicked.connect(lambda *_: self.exit_app.emit())

    def __create_layout(self):
        main_v_layout = QVBoxLayout()

        main_v_layout.addWidget(self.start_app_button)
        main_v_layout.addWidget(QLabel())

        main_v_layout.addWidget(self.set_settings_button)
        main_v_layout.addWidget(QLabel())

        main_v_layout.addWidget(self.exit_app_button)

        self.setLayout(main_v_layout)

    def closeEvent(self, a0: QCloseEvent) -> None:
        self.exit_app.emit()


if __name__ == '__main__':
    qgs_app = QApplication([])

    menu = MainMenuWidget()
    menu.show()

    code = qgs_app.exec_()

