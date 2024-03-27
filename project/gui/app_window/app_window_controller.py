from PyQt5.QtCore import QObject


class AppWindowController(QObject):
    def __init__(self, parent=None):
        super(AppWindowController, self).__init__(parent)
