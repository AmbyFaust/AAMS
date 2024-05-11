import sys

from PyQt5.QtWidgets import QApplication

from project.app_manager import AppManager


def main():

    app = QApplication([])
    app_manager = AppManager(app)
    app_manager.start()
    app.exec_()


if __name__ == '__main__':
    main()