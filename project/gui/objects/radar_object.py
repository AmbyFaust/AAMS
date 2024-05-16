from PyQt5.QtCore import QRectF
from PyQt5.QtGui import QPixmap, QPainterPath
from PyQt5.QtWidgets import QGraphicsPixmapItem

from project import settings
from project.settings import RADAR_ICON_PATH, BASE_SIZE_OBJECT


class RadarObject:
    def __init__(self):
        self.pixmap = QPixmap(RADAR_ICON_PATH)
        self.pixmap.scaled(BASE_SIZE_OBJECT)
        self.radar_item = QGraphicsPixmapItem(self.pixmap)
        self.radar_item.setScale(1)

        self.radius = self.set_radius()
        self.radius_path = QPainterPath()
        # self.radius_path.addEllipse(QRectF(-self.radius, -self.radius, 2 * self.radius, 2 * self.radius))
        self.radar_radius_item = None

    def set_radius(self, eirp = settings.EIRP,
                         seff = settings.SEFF,
                         t_n = settings.T_N,
                         prf = settings.PRF,
                         signal_time = settings.SIGNAL_TIME,
                         n_pulses_proc = settings.N_PULSES_PROC,
                         operating_freq = settings.OPERATING_FREQ,
                         snr_detection = settings.SNR_DETECTION):

        return 100
