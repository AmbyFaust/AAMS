from Object import Object
from collections import namedtuple


radar_params = namedtuple('radar_params', 'EIRP Seff BW_U BW_V')
signal_params = namedtuple('signal_params', 'PRF SignalTime NPulsesProc')
mark = namedtuple('mark', 'U V R stdU stdV stdR')


class RadarObj(Object):

    Trajectories = []
    def __init__(self, start_coords, radar_params, signal_params, start_time):
        self.StartCoords = start_coords
        self.RadarParams = radar_params
        self.SignalParams = signal_params
        self.StartTime = start_time

    def primary_processing(self, target_coords):
        pass

    def secondary_processing(self, marks):
        pass


if __name__ == "__main__":
    start_coords = [0, 0, 0]
    start_time = 0
    RadarParams1 = radar_params(1000, 2, BW_U=0.1, BW_V=0.1)
    Signal1 = signal_params(10^-3, 10^-6, 1000)
    Radar1 = RadarObj(start_time,RadarParams1,Signal1,start_coords)
    # Radar1 = RadarObj()
    print(Radar1 )
