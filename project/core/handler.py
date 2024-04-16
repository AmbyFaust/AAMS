from PyQt5.QtCore import QObject, pyqtSlot, pyqtSignal


class Handler(QObject):
    update_rls = pyqtSignal(dict)

    def __init__(self, parent=None):
        super(Handler, self).__init__(parent)
        self.rls = {}
        self.targets = {}

    @pyqtSlot(object)
    def create_rls(self, rls_object: object):
        self.rls[len(self.rls)] = rls_object
        self.update_rls.emit(self.rls)
        print('РЛС создано')