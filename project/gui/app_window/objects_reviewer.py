from PyQt5.QtWidgets import QListWidget

from project.settings import BASE_FONT


class ObjectsReviewer(QListWidget):

    def __init__(self, *args, **kwargs):
        super(ObjectsReviewer, self).__init__(*args, **kwargs)
        self.setSelectionMode(ObjectsReviewer.SingleSelection)
        self.selected_row = None

        self.setAutoScroll(True)
        self.model().rowsInserted.connect(lambda *_: self.scrollToBottom())

    def update_objects(self, targets, rls):
        self.clear()
        for key, item in rls.items():
            text = 'Тип: РЛС\nid: {}\nx: {}\ny: {}\n'.format(key, 'None', 'None')
            self.addItem(text)
            item = self.item(0)
            item.setFont(BASE_FONT)

        #
        # target_num_to_row = {}
        #
        # for key, info in targets.items():
        #
        #     # dtt_str = f'{year}.{month}.{day} {hour}:{minute}:{second}'
        #     # text = 'Тип {}\nid: {}\nx: {}\ny: {}\n'.format(key, )
        #
        #     self.addItem(text)
        #     item = self.item(self.count() - 1)
        #     item.setFont(LIST_ITEM_FONT)
        #     item.setData(Qt.UserRole, key)
        #     item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
        #     item.setCheckState(Qt.Unchecked)
        #
        #     target_num_to_row[key] = self.count() - 1
        #
        # # выбор строки
        # if self.selected_row is not None:
        #     if 0 <= self.selected_row < self.count():
        #         self.setCurrentRow(self.selected_row)
        #     elif self.count() > 0:
        #         self.selected_row = self.count() - 1
        #         self.setCurrentRow(self.selected_row)
        # # сигнал об окончании обновления списка
        # self.targets_updated.emit()
        # self.send_target_num_to_row.emit(target_num_to_row)



        # self.currentRowChanged.connect(self.__current_row_changed)
        # self.itemClicked.connect(self.__item_clicked)
        # self.itemDoubleClicked.connect(self.__item_double_clicked)

