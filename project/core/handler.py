from PyQt5.QtCore import QObject, pyqtSlot


class Handler(QObject):

    def __init__(self, parent=None):
        super(Handler, self).__init__(parent)
        self.rls = None

    @pyqtSlot()
    def create_rls(self):
        print('РЛС создано')