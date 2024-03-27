from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QCloseEvent
from PyQt5.QtWidgets import QWidget


class QWidgetBase(QWidget):
    close_event_signal = pyqtSignal()

    def __init__(self, parent=None):
        super(QWidgetBase, self).__init__(parent)

    def closeEvent(self, a0: QCloseEvent) -> None:
        self.close_event_signal.emit()

