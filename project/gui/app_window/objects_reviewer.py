from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QListWidget, QAction, QGroupBox, QToolBar, QVBoxLayout, QListWidgetItem

from project.settings import BASE_FONT, EDIT_ICON_PATH, DELETE_ICON_PATH
from project import ObjectEnum


class ObjectsReviewerBox(QGroupBox):
    def __init__(self, type_objects: ObjectEnum, controller):
        super(ObjectsReviewerBox, self).__init__(type_objects.desc)
        self.type_objects = type_objects
        self.controller = controller
        self.__create_widgets()
        self.__create_actions()
        self.__create_tool_bar()
        self.__create_layouts()
        self.setMinimumWidth(300)
        self.setFont(BASE_FONT)

    def __create_widgets(self):
        self.tool_bar = QToolBar()
        self.object_reviewer = ObjectsReviewer(self.type_objects, self.controller)

    def __create_layouts(self):
        common_v_layout = QVBoxLayout()
        common_v_layout.addWidget(self.tool_bar)
        common_v_layout.addWidget(self.object_reviewer)
        self.setLayout(common_v_layout)

    def __create_actions(self):
        self.update_action = QAction('Изменить')
        self.update_action.setIcon(QIcon(EDIT_ICON_PATH))
        self.delete_action = QAction('Удалить')
        self.delete_action.setIcon(QIcon(DELETE_ICON_PATH))

    def __create_tool_bar(self):
        self.tool_bar = QToolBar()
        self.tool_bar.setMovable(False)
        self.tool_bar.addAction(self.update_action)
        self.tool_bar.addAction(self.delete_action)

    def update_objects(self, objects: dict):
        self.object_reviewer.update_objects(objects)


class ObjectsReviewer(QListWidget):
    object_selected = pyqtSignal(int)

    def __init__(self, type_objects: ObjectEnum, controller):
        super(ObjectsReviewer, self).__init__()
        self.type_objects = type_objects
        self.setSelectionMode(ObjectsReviewer.SingleSelection)

        self.selected_row = None
        self.setAutoScroll(True)
        self.controller = controller
        self.model().rowsInserted.connect(lambda *_: self.scrollToBottom())

        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.__create_actions()

        self.currentRowChanged.connect(self.__current_row_changed)
        self.itemClicked.connect(self.__item_clicked)
        self.itemDoubleClicked.connect(self.__item_double_clicked)

    def __create_actions(self):
        self.update_action = QAction('Изменить')
        self.update_action.setIcon(QIcon(EDIT_ICON_PATH))
        self.delete_action = QAction('Удалить')
        self.delete_action.setIcon(QIcon(DELETE_ICON_PATH))

    def update_objects(self, objects):
        try:
            self.clear()

            for key, item in objects.items():
                # self.addItem(ObjectInfoWidgetItem(None, self.controller, self))
                text = 'Тип: {}\nid: {}\nx: {}\ny: {}\n'.format(self.type_objects.desc, key, 'None', 'None')
                self.addItem(text)
                item = self.item(self.count() - 1)
                item.setFont(BASE_FONT)
                item.setData(Qt.UserRole, key)

            # выбор строки
            if self.selected_row is not None:
                if 0 <= self.selected_row < self.count():
                    self.setCurrentRow(self.selected_row)
                elif self.count() > 0:
                    self.selected_row = self.count() - 1
                    self.setCurrentRow(self.selected_row)

        except BaseException as exp:
            print(f'Ошибка в обновлении объектов в листе: {exp}')

    def __current_row_changed(self, row: int):
        if row is None:
            return

        if 0 <= row < self.count():
            self.selected_row = row
            item = self.item(row)
            if item is None:
                return
            key = item.data(Qt.UserRole)
            if key is not None:
                self.object_selected.emit(key)

    def __item_clicked(self, item: QListWidgetItem):
        pass

    def __item_double_clicked(self, item: QListWidgetItem):
        if item is None:
            return

        self.__item_clicked(item)
        self.__current_row_changed(self.row(item))
