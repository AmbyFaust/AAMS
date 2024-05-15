from collections import namedtuple


# объявляем используемые типы данных
radar_params = namedtuple('radar_params', 'EIRP Seff  BW_U BW_V Scanning_V Tn PRF SignalTime NPulsesProc OperatingFreq '
                                          'start_time start_coords SNRDetection')
mark = namedtuple('mark', 'U V R stdU stdV stdR TargetId')
target_params = namedtuple('target_params', 'RCS coordinates TargetId')
RectCS = namedtuple('RectCS', 'X Y Z')
UVCS = namedtuple('UVCS', 'U V R')
trajectory = namedtuple('trajectory','stack_of_coords ,target_id, is_confimed')


if __name__ == "__main__":
    Coordinate1 = RectCS(X=10, Y=5, Z=6)


