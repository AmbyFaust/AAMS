import os

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QGraphicsView, QHBoxLayout, QWidget, QVBoxLayout, QLabel, QAction, QToolBar, QGroupBox, \
    QLineEdit, QPushButton, QFileDialog

from project import ObjectEnum
from project.gui.app_window.controller import Controller
from project.gui.app_window.map_scene import GridScene
from project.gui.app_window.objects_reviewer import ObjectsReviewer, ObjectsReviewerBox
from project.gui.base_form_classes import QMainWindowBase
from project.settings import BASE_FONT, SAR_ICON_PATH, TARGET_ICON_PATH, INPUT_FILE_PATH


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
        self.controller.remove_gui_target.connect(self.map.remove_object)
        self.controller.remove_gui_sar.connect(self.map.remove_object)
        self.controller.redraw_sar.connect(self.map.redraw_sar)

    def __create_widgets(self):
        settings_action = QAction("Настройки", self)
        # settings_action.triggered.connect()

        self.map = GridScene(self, self.controller)
        self.map_view = QGraphicsView(self.map)
        self.map_view.setGeometry(0, 0, 1300, 900)
        self.map.draw_grid(self.map_view.size())
        self.map.get_current_coordinates.connect(self.__update_coordinates_widgets)

        self.sar_reviewer = ObjectsReviewerBox(ObjectEnum.SAR, self.controller)
        self.sar_reviewer.object_reviewer.object_selected.connect(self.__sar_selected)

        self.target_reviewer = ObjectsReviewerBox(ObjectEnum.TARGET, self.controller)
        self.target_reviewer.object_reviewer.object_selected.connect(self.__target_selected)

        self.x_label = QLabel('X: ')
        self.x_label.setFont(BASE_FONT)
        self.y_label = QLabel('Y: ')
        self.y_label.setFont(BASE_FONT)

        self.x_line_edit = QLineEdit()
        self.x_line_edit.setFont(BASE_FONT)
        self.x_line_edit.setReadOnly(True)

        self.y_line_edit = QLineEdit()
        self.y_line_edit.setFont(BASE_FONT)
        self.y_line_edit.setReadOnly(True)

        self.calculate_btn = QPushButton('Рассчитать')
        self.calculate_btn.setFont(BASE_FONT)
        self.modeling_btn = QPushButton('Моделирование')
        self.modeling_btn.setFont(BASE_FONT)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

    def __create_layout(self):
        coordinates_h_layout = QHBoxLayout()
        coordinates_h_layout.addWidget(self.x_label)
        coordinates_h_layout.addWidget(self.x_line_edit)
        coordinates_h_layout.addWidget(self.y_label)
        coordinates_h_layout.addWidget(self.y_line_edit)

        map_v_layout = QVBoxLayout()
        map_v_layout.addWidget(self.map_view)
        map_v_layout.addLayout(coordinates_h_layout)

        btn_h_layout = QHBoxLayout()
        btn_h_layout.addWidget(self.calculate_btn)
        btn_h_layout.addWidget(self.modeling_btn)

        objects_v_layout = QVBoxLayout()
        objects_v_layout.addWidget(self.tool_bar)
        objects_v_layout.addWidget(self.sar_reviewer)
        objects_v_layout.addWidget(self.target_reviewer)
        objects_v_layout.addLayout(btn_h_layout)

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

        self.calculate_btn.clicked.connect(self.__calculate)
        self.modeling_btn.clicked.connect(self.__modeling)

    def __create_toolbar(self):
        self.tool_bar = QToolBar()
        self.tool_bar.setMovable(False)
        self.tool_bar.addAction(self.create_target_path_action)
        self.tool_bar.addAction(self.create_sar_action)

    def __calculate(self):
        pass

    def __modeling(self):
        print(INPUT_FILE_PATH)

    @pyqtSlot(int, int)
    def __update_coordinates_widgets(self, x_position: int, y_position: int):
        self.x_line_edit.setText(f'{x_position}')
        self.y_line_edit.setText(f'{y_position}')

    def __create_sar(self):
        if self.map.current_obj_type is None:
            self.map.current_obj_type = ObjectEnum.SAR

    def __create_target(self):
        if self.map.current_obj_type is None:
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
