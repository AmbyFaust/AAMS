import numpy as np
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
        self.radar_radius_item = None

    @staticmethod
    def set_radius(eirp=settings.EIRP,
                   seff=settings.SEFF,
                   t_n=settings.T_N,
                   signal_time=settings.SIGNAL_TIME,
                   n_pulses_proc=settings.N_PULSES_PROC,
                   snr_detection=settings.SNR_DETECTION,
                   RCS=settings.EPR):
        print(eirp)
        # DetRange = ((eirp * seff * n_pulses_proc * RCS * signal_time) /
        #           (((4 * np.pi) ** 2)*snr_detection * 1.38*10**-23 *t_n))**1/4

        DetRange = ((eirp * seff * n_pulses_proc * RCS * signal_time) / (
                    (4 * np.pi) ** 2 * snr_detection * 1.38 * 10 ** -23 * t_n)) ** (1 / 4)
        # print(DetRange)
        return 100
