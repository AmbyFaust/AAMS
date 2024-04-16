from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QListWidget, QAction, QGroupBox, QToolBar, QVBoxLayout

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
        self.redact_action = QAction('Изменить')
        self.redact_action.triggered.connect(self.edit_object)
        self.redact_action.setIcon(QIcon(EDIT_ICON_PATH))
        self.delete_action = QAction('Удалить')
        self.delete_action.triggered.connect(self.delete_object)
        self.delete_action.setIcon(QIcon(DELETE_ICON_PATH))

    def edit_object(self):
        pass

    def delete_object(self):
        pass

    def __create_tool_bar(self):
        self.tool_bar = QToolBar()
        self.tool_bar.setMovable(False)
        self.tool_bar.addAction(self.redact_action)
        self.tool_bar.addAction(self.delete_action)

    def update_objects(self, objects: dict):
        self.object_reviewer.update_objects(objects)


class ObjectsReviewer(QListWidget):
    def __init__(self, type_objects: ObjectEnum, controller):
        super(ObjectsReviewer, self).__init__()
        self.type_objects = type_objects
        self.setSelectionMode(ObjectsReviewer.SingleSelection)
        self.setAutoScroll(True)
        self.controller = controller
        self.model().rowsInserted.connect(lambda *_: self.scrollToBottom())

        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.__create_actions()

    def __create_actions(self):
        self.redact_action = QAction('Изменить')
        self.redact_action.triggered.connect(self.edit_object)
        self.delete_action = QAction('Удалить')
        self.delete_action.triggered.connect(self.delete_object)

    def edit_object(self):
        pass

    def delete_object(self):
        pass

    def update_objects(self, objects):
        self.clear()
        index = 0
        for key, item in objects.items():
            # self.addItem(ObjectInfoWidgetItem(None, self.controller, self))
            text = 'Тип: {}\nid: {}\nx: {}\ny: {}\n'.format(self.type_objects.desc, key, 'None', 'None')
            self.addItem(text)
            item = self.item(index)
            item.setFont(BASE_FONT)

            index += 1
