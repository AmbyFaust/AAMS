from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QFileDialog


class QOpenFilesDialog(QFileDialog):
    def __init__(self, *args, **kwargs):
        super(QOpenFilesDialog, self).__init__(*args, **kwargs)
        self.setWindowModality(Qt.ApplicationModal)
        self.setOption(QFileDialog.DontUseNativeDialog)

        self.setLabelText(QFileDialog.LookIn, 'Открыть')
        self.setLabelText(QFileDialog.Accept, 'Открыть')
        self.setLabelText(QFileDialog.Reject, 'Отмена')