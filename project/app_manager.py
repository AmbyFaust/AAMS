from PyQt5.QtCore import QObject, pyqtSlot
from PyQt5.QtWidgets import QDialog

from project.core.handler import Handler
from project.gui import SettingsDialog, MainMenuWidget, AppWindow


class AppManager(QObject):
    """
    Диспетчер приложения
    """

    def __init__(self, application):
        super(AppManager, self).__init__(application)

        # создание графического интерфейса
        self.__create_gui()

        # создание сервисов
        self.__create_services()

        # настройка связи между gui и сервисами
        self.__connect_gui_services()



    def start(self):
        self.main_menu_widget.show()

    def __create_gui(self):
        self.main_menu_widget = MainMenuWidget()
        self.main_menu_widget.start_app.connect(self.__start_app)
        self.main_menu_widget.set_settings.connect(self.__set_settings)
        self.main_menu_widget.exit_app.connect(self.__exit_app)

        self.app_window = AppWindow()

    def __create_services(self):
        self.handler = Handler()

    @pyqtSlot()
    def __set_settings(self):
        dialog = SettingsDialog()
        if dialog.exec() == QDialog.Accepted:
            pass

    def __start_app(self):
        self.app_window.showMaximized()
        self.main_menu_widget.hide()

    def __exit_app(self):
        self.app_window.close()
        self.main_menu_widget.close()

    def __connect_gui_services(self):
        self.app_window.controller.create_rls.connect(self.handler.create_rls)
        self.handler.update_rls.connect(self.app_window.controller.update_rls_reviewer)


