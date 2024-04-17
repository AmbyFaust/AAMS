from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QGraphicsView, QHBoxLayout, QWidget, QVBoxLayout, QLabel, QAction, QToolBar, QGroupBox

from project import ObjectEnum
from project.gui.app_window.controller import Controller
from project.gui.app_window.map_scene import GridScene
from project.gui.app_window.objects_reviewer import ObjectsReviewer, ObjectsReviewerBox
from project.gui.base_form_classes import QMainWindowBase
from project.settings import BASE_FONT, SAR_ICON_PATH, TARGET_ICON_PATH


class AppWindow(QMainWindowBase):
    """
    Главное окно приложения
    """
    def __init__(self, parent=None):
        super(AppWindow, self).__init__(parent)

        self.setGeometry(100, 100, 800, 600)
        self.setWindowTitle('AAMS')

        # контроллер главного окна приложения
        self.controller = Controller()

        self.__create_widgets()
        self.__create_action()
        self.__create_toolbar()
        self.__create_layout()

        # соединение контроллера с другими объектами
        self.controller.update_sar_list.connect(self.sar_reviewer.update_objects)
        self.controller.update_targets_list.connect(self.target_reviewer.update_objects)

    def __create_widgets(self):
        settings_action = QAction("Настройки", self)
        # settings_action.triggered.connect()

        self.map = GridScene(self, self.controller)
        self.map_view = QGraphicsView(self.map)
        self.map_view.setGeometry(0, 0, 1300, 900)
        self.map.draw_grid(self.map_view.size())

        self.sar_reviewer = ObjectsReviewerBox(ObjectEnum.SAR, self.controller)
        self.sar_reviewer.object_reviewer.object_selected.connect(self.__sar_selected)

        self.target_reviewer = ObjectsReviewerBox(ObjectEnum.TARGET, self.controller)
        self.target_reviewer.object_reviewer.object_selected.connect(self.__target_selected)

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
        objects_v_layout.addWidget(self.sar_reviewer)
        objects_v_layout.addWidget(self.target_reviewer)

        common_h_layout = QHBoxLayout()
        common_h_layout.addLayout(map_v_layout)
        common_h_layout.addLayout(objects_v_layout)

        self.central_widget.setLayout(common_h_layout)

    def __create_action(self):
        self.create_target_path_action = QAction('Установить путь цели')
        self.create_target_path_action.setIcon(QIcon(TARGET_ICON_PATH))
        self.create_target_path_action.triggered.connect(self.__create_target)

        self.create_sar_action = QAction('Установить РЛС')
        self.create_sar_action.setIcon(QIcon(SAR_ICON_PATH))
        self.create_sar_action.triggered.connect(self.__create_sar)

        self.sar_reviewer.delete_action.triggered.connect(self.__remove_sar_action_triggered)
        self.target_reviewer.delete_action.triggered.connect(self.__remove_target_action_triggered)
        self.sar_reviewer.update_action.triggered.connect(self.__update_sar_action_triggered)
        self.target_reviewer.update_action.triggered.connect(self.__update_target_action_triggered)

    def __create_toolbar(self):
        self.tool_bar = QToolBar()
        self.tool_bar.setMovable(False)
        self.tool_bar.addAction(self.create_target_path_action)
        self.tool_bar.addAction(self.create_sar_action)

    def __create_sar(self):
        self.map.current_obj_type = ObjectEnum.SAR
        # self.controller.create_object(ObjectEnum.RLS)

    def __create_target(self):
        self.map.current_obj_type = ObjectEnum.TARGET

    def __sar_selected(self, sar_id: int):
        self.controller.is_sar_selected(sar_id)

    def __target_selected(self, target_id: int):
        self.controller.is_target_selected(target_id)

    def __remove_sar_action_triggered(self):
        self.controller.remove_selected_sar()

    def __remove_target_action_triggered(self):
        self.controller.remove_selected_target()

    def __update_sar_action_triggered(self):
        self.controller.update_selected_sar()

    def __update_target_action_triggered(self):
        self.controller.update_selected_target()
