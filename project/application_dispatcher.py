from PyQt5.QtCore import QObject


class ApplicationDispatcher(QObject):
    """
    Диспетчер приложения
    """

    def __init__(self, application):
        super(ApplicationDispatcher, self).__init__(application)

        # создание графического интерфейса
        self.__create_gui()

        # создание сервисов
        self.__create_services()

        # настройка связи между gui и сервисами
        self.__connect_gui_services()

    def __create_gui(self):
        pass

    def __create_services(self):
        pass

    def __connect_gui_services(self):
        pass
