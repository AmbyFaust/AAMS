from PyQt5.QtCore import QPoint, QSize
from PyQt5.QtWidgets import QWidget


class ObjectWidgetBase(QWidget):

    def __init__(self, pos: QPoint, icon_path: str):
        self.pos = pos
        self.icon_path = icon_path
        self.size = QSize(25, 25)

