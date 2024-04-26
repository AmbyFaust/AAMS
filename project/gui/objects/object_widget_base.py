from PyQt5.QtCore import QPoint, QSize
from PyQt5.QtWidgets import QWidget

from project import settings


class ObjectWidgetBase(QWidget):

    def __init__(self, parent=None, *, pos: QPoint, icon_path: str):
        super(ObjectWidgetBase, self).__init__(parent)
        self.pos = pos
        self.icon_path = icon_path
        self.size = settings.BASE_SIZE_OBJECT

