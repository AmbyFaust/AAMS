import os
import pandas as pd

from PyQt5.QtCore import pyqtSlot, Qt, QTimer
from PyQt5.QtGui import QIcon, QPen
from PyQt5.QtWidgets import QGraphicsView, QHBoxLayout, QWidget, QVBoxLayout, QLabel, QAction, QToolBar, QGroupBox, \
    QLineEdit, QPushButton, QFileDialog, QProgressBar, QSlider, QGraphicsLineItem, QApplication

from project import ObjectEnum
from project.gui.app_window.controller import Controller
from project.gui.app_window.map_scene import GridScene
from project.gui.app_window.objects_reviewer import ObjectsReviewer, ObjectsReviewerBox
from project.gui.base_form_classes import QMainWindowBase
from project.settings import BASE_FONT, RADAR_ICON_PATH, TARGET_ICON_PATH, INPUT_FILE_PATH


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
        self.__create_actions()
        self.__create_toolbar()
        self.__create_layout()

        self.dataframe = None
        self.is_paused = True
        self.lines = []
        self.current_index = 0

        # соединение контроллера с другими объектами
        self.controller.update_radar_list.connect(self.radar_reviewer.update_objects)
        self.controller.update_targets_list.connect(self.target_reviewer.update_objects)
        self.controller.remove_gui_target.connect(self.map.remove_object)
        self.controller.remove_gui_radar.connect(self.map.remove_object)
        self.controller.redraw_radar.connect(self.map.redraw_radar)

        self.modelling_timer = QTimer()
        self.modelling_timer.timeout.connect(self.__update_slider_progress)

    def __create_widgets(self):
        settings_action = QAction("Настройки", self)
        # settings_action.triggered.connect()

        self.map = GridScene(self, self.controller)
        self.map_view = QGraphicsView(self.map)
        self.map_view.setGeometry(0, 0, 13000, 9000)
        self.map.draw_grid(self.map_view.size())
        self.map.get_current_coordinates.connect(self.__update_coordinates_widgets)

        self.radar_reviewer = ObjectsReviewerBox(ObjectEnum.RADAR, self.controller)
        self.radar_reviewer.object_reviewer.object_selected.connect(self.__radar_selected)

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

        self.start_button = QPushButton('Старт')
        self.start_button.setEnabled(False)
        self.start_button.clicked.connect(self.__toggle_modelling)

        self.slider_progress = QSlider(Qt.Horizontal)
        self.slider_progress.setRange(0, 1)
        self.slider_progress.setEnabled(False)
        self.slider_progress.valueChanged.connect(self.__update_scene_modelling)

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

        scroll_h_layout = QHBoxLayout()
        scroll_h_layout.addWidget(self.start_button)
        scroll_h_layout.addWidget(self.slider_progress)

        btn_h_layout = QHBoxLayout()
        btn_h_layout.addWidget(self.calculate_btn)
        btn_h_layout.addWidget(self.modeling_btn)

        objects_v_layout = QVBoxLayout()
        objects_v_layout.addWidget(self.tool_bar)
        objects_v_layout.addWidget(self.radar_reviewer)
        objects_v_layout.addWidget(self.target_reviewer)
        objects_v_layout.addLayout(scroll_h_layout)
        objects_v_layout.addLayout(btn_h_layout)

        common_h_layout = QHBoxLayout()
        common_h_layout.addLayout(map_v_layout)
        common_h_layout.addLayout(objects_v_layout)

        self.central_widget.setLayout(common_h_layout)

    def __create_actions(self):
        self.create_target_path_action = QAction('Установить путь цели')
        self.create_target_path_action.setIcon(QIcon(TARGET_ICON_PATH))
        self.create_target_path_action.triggered.connect(self.__create_target)

        self.create_radar_action = QAction('Установить РЛС')
        self.create_radar_action.setIcon(QIcon(RADAR_ICON_PATH))
        self.create_radar_action.triggered.connect(self.__create_radar)

        self.radar_reviewer.delete_action.triggered.connect(self.__remove_radar_action_triggered)
        self.target_reviewer.delete_action.triggered.connect(self.__remove_target_action_triggered)

        self.radar_reviewer.update_action.triggered.connect(self.__update_radar_action_triggered)
        self.target_reviewer.update_action.triggered.connect(self.__update_target_action_triggered)

        self.calculate_btn.clicked.connect(self.__calculate)
        self.modeling_btn.clicked.connect(self.__modeling)

    def __create_toolbar(self):
        self.tool_bar = QToolBar()
        self.tool_bar.setMovable(False)
        self.tool_bar.addAction(self.create_target_path_action)
        self.tool_bar.addAction(self.create_radar_action)

    def __calculate(self):
        self.controller.calculate_signal.emit()

    def __modeling(self):
        self.controller.modeling_signal.emit()

    @pyqtSlot(int, int)
    def __update_coordinates_widgets(self, x_position: int, y_position: int):
        self.x_line_edit.setText(f'{x_position}')
        self.y_line_edit.setText(f'{y_position}')

    def __create_radar(self):
        if self.map.current_obj_type is None:
            self.map.current_obj_type = ObjectEnum.RADAR

    def __create_target(self):
        if self.map.current_obj_type is None:
            self.map.current_obj_type = ObjectEnum.TARGET

    def __radar_selected(self, radar_id: int):
        self.controller.is_radar_selected(radar_id)

    def __target_selected(self, target_id: int):
        self.controller.is_target_selected(target_id)

    def __remove_radar_action_triggered(self):
        self.controller.remove_selected_radar()

    def __remove_target_action_triggered(self):
        self.controller.remove_selected_target()

    def __update_radar_action_triggered(self):
        self.controller.update_selected_radar()

    def __update_target_action_triggered(self):
        self.controller.update_selected_target()

    def __toggle_modelling(self):
        if self.is_paused:
            self.__start_slider_progress()
        else:
            self.__pause_slider_progress()

    def __start_slider_progress(self):
        self.start_button.setText('Стоп')
        self.is_paused = False
        self.modelling_timer.start(1)

    def __pause_slider_progress(self):
        self.start_button.setText('Старт')
        self.is_paused = True
        self.modelling_timer.stop()

    def __update_slider_progress(self):
        current_value = self.slider_progress.value()

        if current_value >= len(self.dataframe) - 1:
            self.__pause_slider_progress()
            self.slider_progress.setValue(len(self.dataframe) - 1)
        else:
            self.slider_progress.setValue(current_value + 1)

    @pyqtSlot(object)
    def load_modelling_dataframe(self, dataframe: pd.DataFrame):
        self.map.remove_targets()

        self.dataframe = dataframe

        self.slider_progress.setRange(0, len(self.dataframe) - 1)
        self.slider_progress.setEnabled(True)
        self.start_button.setEnabled(True)

    @pyqtSlot(int)
    def __update_scene_modelling(self, slider_progress_value: int):
        try:
            if slider_progress_value > self.current_index:
                for i in range(self.current_index, slider_progress_value):
                    if i + 1 < len(self.dataframe):
                        x1, y1 = self.dataframe.iloc[i]['x'], self.dataframe.iloc[i]['y']
                        x2, y2 = self.dataframe.iloc[i + 1]['x'], self.dataframe.iloc[i + 1]['y']

                        line = QGraphicsLineItem(x1, y1, x2, y2)
                        pen = QPen(Qt.black, 2)
                        line.setPen(pen)
                        self.map.addItem(line)
                        self.lines.append(line)

            else:
                for i in range(self.current_index - 1, slider_progress_value, -1):
                    if self.lines:
                        line = self.lines.pop()
                        self.map.removeItem(line)

            self.current_index = slider_progress_value

        except BaseException as exp:
            print(exp)