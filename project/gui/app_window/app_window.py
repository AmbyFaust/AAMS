from project.gui.base_form_classes import QMainWindowBase


class AppWindow(QMainWindowBase):
    """
    Главное окно приложения
    """
    def __init__(self, parent=None):
        super(AppWindow, self).__init__(parent)
        self.setWindowTitle('AAMS')
        self.__create_controler()
        self.__create_widgets()
        self.__create_layout()

    def __create_controller(self):
        pass

    def __create_widgets(self):
        pass

    def __create_layout(self):
        pass