from project.modeling.ObjectModels.RadarObj import RadarObj
from project.modeling.ObjectModels.SimpleTestPlane import SimpleTestPlane
from project.modeling.ObjectModels.DataStructures import radar_params, UVCS, RectCS

start_coords = RectCS(0, 0, 0)
start_time = 0
RadarParams1 = radar_params(1000, 2, BW_U=3, BW_V=3, Scanning_V=[10, 70],
                            Tn=1000, PRF=10 ** 3, SignalTime=10 ** (-6), NPulsesProc=1000, OperatingFreq=15 * 10 ** 9,
                            start_time=start_time, start_coords=start_coords, SNRDetection=12)

Radar1 = RadarObj(RadarParams1)
testPlane1 = SimpleTestPlane()
print(Radar1)
print(testPlane1)
timesdiskret = 10 ** -2
targets = [testPlane1]
time = 0
while time < 100:
    Radar1.MakeMeasurement(targets, time)
    time += timesdiskret
