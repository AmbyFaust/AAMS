import os

from PyQt5.QtCore import QSize
from PyQt5.QtGui import QFont

from project import TypeTargetEnum

BASE_FONT = QFont('Ms Shell Dlg', 11)

BASE_SIZE_OBJECT = QSize(50, 50)

TARGET_POINT_RADIUS = 12

RADAR_ICON_PATH = './project/static/radar.svg'
TARGET_ICON_PATH = './project/static/target.svg'
EDIT_ICON_PATH = './project/static/edit.svg'
DELETE_ICON_PATH = './project/static/delete.svg'


INPUT_FILE_PATH = os.path.join(os.getcwd(), 'results')

# Радар
EIRP = 10**5
SEFF = 3
BW_U = 3
BW_V = 3
SCANNING_V = [0, 60]
T_N = 1000
PRF = 10**6
SIGNAL_TIME = 10**(-6)
N_PULSES_PROC = 1000
OPERATING_FREQ = 15*10**9
START_TIME = 0
SNR_DETECTION = 10

# Цель
SPEED = 200
TARGET_TYPE = TypeTargetEnum.first
EPR = 10
HEIGHT = 5000
