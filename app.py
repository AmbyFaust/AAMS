import logging
import sys

from PyQt5.QtWidgets import QApplication

from project.app_manager import AppManager


def main():

    app = QApplication([])
    app_manager = AppManager(app)
    app_manager.start()
    app.exec_()


if __name__ == '__main__':
    # logging.basicConfig(level=logging.INFO, filename="py_log.log", filemode="w", encoding="utf-8",
    #                      format="%(asctime)s %(levelname)s %(message)s")
    main()