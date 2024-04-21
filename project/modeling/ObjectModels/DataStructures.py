from collections import namedtuple
# объявляем используемые типы данных
radar_params = namedtuple('radar_params', 'EIRP Seff  BW_U BW_V Scanning_V Tn')
# radar_params = namedtuple('radar_params', 'EIRP Seff BW_U BW_V Tn')
signal_params = namedtuple('signal_params', 'PRF SignalTime NPulsesProc OperatingFreq')
mark = namedtuple('mark', 'U V R stdU stdV stdR')
target_params = namedtuple('target_params', 'RCS coordinates')
RectCS = namedtuple('RectCS', 'X Y Z')
UVCS = namedtuple('UVCS', 'U V R')
