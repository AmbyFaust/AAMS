from PyQt5.QtCore import QRectF
from PyQt5.QtGui import QPixmap, QPainterPath
from PyQt5.QtWidgets import QGraphicsPixmapItem

from project.settings import RADAR_ICON_PATH, BASE_SIZE_OBJECT


class RadarObject:
    def __init__(self):
        self.pixmap = QPixmap(RADAR_ICON_PATH)
        self.pixmap.scaled(BASE_SIZE_OBJECT)
        self.radar_item = QGraphicsPixmapItem(self.pixmap)
        self.radar_item.setScale(1)

        self.radius_path = QPainterPath()
        self.radius_path.addEllipse(QRectF(-100, -100, 2 * 100, 2 * 100))
        self.radar_radius_item = None

