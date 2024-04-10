from collections import namedtuple

from Object import Object


radar_params = namedtuple('radar_params', 'EIRP Seff BW_U BW_V')
signal_params = namedtuple('signal_params', 'PRF SignalTime NPulsesProc')
mark = namedtuple('mark', 'U V R stdU stdV stdR')
RCS = namedtuple('RCScoords','X Y Z')
UVcoords = ('UVcoords', 'U V R')

class MakeMeasurement():
    pass

class RadarObj(Object):

    Trajectories = []
    def __init__(self, start_coords, radar_params, signal_params, start_time):
        self.StartCoords = start_coords
        self.RadarParams = radar_params
        self.SignalParams = signal_params
        self.StartTime = start_time

    def GRCStoLRCS(self, targets_coordsGRCS):
        targets_coordsGRCS = [None] * len(targets_coordsGRCS)
        for i in range(len(targets_coordsGRCS)):
            targets_coordsGRCS[i] = RCS(X=targets_coordsGRCS[i].X - self.StartCoords.X,
                                                       Y=targets_coordsGRCS[i].Y - self.StartCoords.Y,
                                                       Z=targets_coordsGRCS[i].Z - self.StartCoords.Z)
        return targets_coordsGRCS



if __name__ == "__main__":
    start_coords = RCS(0,0,0)
    start_time = 0
    RadarParams1 = radar_params(1000, 2, BW_U=0.1, BW_V=0.1)
    Signal1 = signal_params(10^-3, 10^-6, 1000)
    Radar1 = RadarObj(start_time,RadarParams1,Signal1,start_coords)
    # Radar1 = RadarObj()
    print(Radar1 )
