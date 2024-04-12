from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtWidgets import QGraphicsView, QHBoxLayout, QWidget, QVBoxLayout, QLabel, QAction, QToolBar


from project.gui.app_window.map_scene import GridScene
from project.gui.app_window.objects_reviewer import ObjectsReviewer
from project.gui.base_form_classes import QMainWindowBase
from project.gui.settings import BASE_FONT


class AppWindow(QMainWindowBase):
    """
    Главное окно приложения
    """
    def __init__(self, parent=None):
        super(AppWindow, self).__init__(parent)

        self.setGeometry(100, 100, 800, 600)
        self.setWindowTitle('AAMS')
        self.__create_controller()
        self.__create_widgets()
        self.__create_action()
        self.__create_toolbar()
        self.__create_layout()

    def __create_controller(self):
        pass

    def __create_widgets(self):
        settings_action = QAction("Настройки", self)
        # settings_action.triggered.connect()

        main_menu = self.menuBar()
        main_menu.setFont(BASE_FONT)
        main_menu.addAction(settings_action)

        self.map = GridScene(self)
        self.map_view = QGraphicsView(self.map)
        self.map_view.setGeometry(0, 0, 1300, 900)
        self.map.drawGrid(self.map_view.size())

        self.objects_reviewer = ObjectsReviewer()
        self.objects_reviewer.setMinimumWidth(300)

        self.x_label = QLabel('X: ')
        self.x_label.setFont(BASE_FONT)
        self.y_label = QLabel('Y: ')
        self.y_label.setFont(BASE_FONT)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

    def __create_layout(self):
        coords_h_layout = QHBoxLayout()
        coords_h_layout.addWidget(self.x_label)
        coords_h_layout.addWidget(self.y_label)

        map_v_layout = QVBoxLayout()
        map_v_layout.addWidget(self.map_view)
        map_v_layout.addLayout(coords_h_layout)

        objects_v_layout = QVBoxLayout()
        objects_v_layout.addWidget(self.tool_bar)
        objects_v_layout.addWidget(self.objects_reviewer)

        common_h_layout = QHBoxLayout()
        common_h_layout.addLayout(map_v_layout)
        common_h_layout.addLayout(objects_v_layout)

        self.central_widget.setLayout(common_h_layout)

    def __create_action(self):
        self.create_object_action = QAction('Установить объект')
        self.create_object_action.setIcon(QIcon('./project/static/create_object_icon.png'))

    def __create_toolbar(self):
        self.tool_bar = QToolBar()
        self.tool_bar.setMovable(False)
        self.tool_bar.addAction(self.create_object_action)



