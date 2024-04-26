from PyQt5.QtCore import QPoint
from PyQt5.QtGui import QPixmap

from project.gui.objects import ObjectWidgetBase


class SarWidget(ObjectWidgetBase):
    def __init__(self, parent=None, *, pos: QPoint, icon_path: str, radius: int):
        super(SarWidget, self).__init__(parent, pos=pos, icon_path=icon_path)
        self.radius = radius

        self.__create_sar_widget()

    def __create_sar_widget(self):
        pixmap = QPixmap(self.icon_path)

        pixmap.scaled(self.size)


        self.current_object = QGraphicsPixmapItem(pixmap)
        self.current_object.setScale(1)
        self.current_object.setPos(
            event.scenePos() - QPoint(BASE_SIZE_OBJECT.width() // 2, BASE_SIZE_OBJECT.height() // 2))
        self.addItem(self.current_object)
