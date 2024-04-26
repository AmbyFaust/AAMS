from PyQt5.QtCore import QRectF
from PyQt5.QtGui import QPixmap, QPainterPath
from PyQt5.QtWidgets import QGraphicsPixmapItem

from project.settings import SAR_ICON_PATH, BASE_SIZE_OBJECT, SAR_RADIUS


class SarObject:
    def __init__(self):
        self.pixmap = QPixmap(SAR_ICON_PATH)
        self.pixmap.scaled(BASE_SIZE_OBJECT)
        self.sar_item = QGraphicsPixmapItem(self.pixmap)
        self.sar_item.setScale(1)

        self.radar_path = QPainterPath()
        self.radar_path.addEllipse(QRectF(-SAR_RADIUS, -SAR_RADIUS, 2 * SAR_RADIUS, 2 * SAR_RADIUS))
        self.radar_item = None

