import os

from PyQt5.QtCore import QSize
from PyQt5.QtGui import QFont

BASE_FONT = QFont('Ms Shell Dlg', 11)

BASE_SIZE_OBJECT = QSize(50, 50)

TARGET_POINT_RADIUS = 12

SAR_ICON_PATH = './project/static/sar.svg'
TARGET_ICON_PATH = './project/static/target.svg'
EDIT_ICON_PATH = './project/static/edit.svg'
DELETE_ICON_PATH = './project/static/delete.svg'


INPUT_FILE_PATH = os.path.join(os.getcwd(), 'results')
SAR_RADIUS = 50
