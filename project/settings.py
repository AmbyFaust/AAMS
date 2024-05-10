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
EIRP = 10
SEFF = 10
BW_U = 10
BW_V = 10
SCANNING_V = [1, 44]
T_N = 280
PRF = 1
SIGNAL_TIME = 1.0
N_PULSES_PROC = 20
OPERATING_FREQ = 200
START_TIME = 0
SNR_DETECTION = 10

# Цель
SPEED = 100
TARGET_TYPE = TypeTargetEnum.first
EPR = 100
HEIGHT = 100
