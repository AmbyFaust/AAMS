from project.modeling.ObjectModels.RadarObj import RadarObj
from project.modeling.ObjectModels.SimpleTestPlane import SimpleTestPlane
from project.modeling.ObjectModels.DataStructures import radar_params, UVCS, RectCS
import numpy as np
start_coords = RectCS(0, 0, 0)
start_time = 0
RadarParams1 = radar_params(EIRP = 100000, Seff = 2, BW_U=3, BW_V=3, Scanning_V=[10, 70],
                            Tn=1000, PRF=10 ** 5, SignalTime=10 ** (-6), NPulsesProc=1000, OperatingFreq=15 * 10 ** 9,
                            start_time=start_time, start_coords=start_coords, SNRDetection=12)

Radar1 = RadarObj(RadarParams1)
testPlane1 =SimpleTestPlane(RectCS(4000, 400, 2000),RectCS(20, 10, 0),10)
print(Radar1)
print(testPlane1)
overall_time = 20
t_btw_scanning = 1000 * (1 / 10 ** 5)
time = np.linspace(0, overall_time, int(overall_time / t_btw_scanning) + 1)
targets = [testPlane1]
for timediskr in time:
    # print(timediskr)
    Radar1.MakeMeasurement(targets, timediskr)
