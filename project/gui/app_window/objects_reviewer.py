from PyQt5.QtWidgets import QListWidget


class ObjectsReviewer(QListWidget):

    def __init__(self, *args, **kwargs):
        super(ObjectsReviewer, self).__init__(*args, **kwargs)
        self.setSelectionMode(ObjectsReviewer.SingleSelection)
        self.selected_row = None

        self.setAutoScroll(True)
        self.model().rowsInserted.connect(lambda *_: self.scrollToBottom())

        # self.currentRowChanged.connect(self.__current_row_changed)
        # self.itemClicked.connect(self.__item_clicked)
        # self.itemDoubleClicked.connect(self.__item_double_clicked)