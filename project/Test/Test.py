import math
import numpy as np
from project.modeling.ObjectModels.RadarObj import RadarObj,mark,radar_params,signal_params,RectCS
from project.modeling.CSTransformator import GRCStoUV
from project.modeling.CSTransformator import UVtoGRCS

start_coords = RectCS(0, 0, 0)
start_time = 0
RadarParams1 = radar_params(1000, 2, BW_U=3, BW_V=3, Scanning_V=[10,70])
PRF = 10 ** 5
SignalTime = 10 ** (-6)
NPulsesProc = 1000
OperatingFreq = 15 * 10 ** 9
Signal1 = signal_params(PRF, SignalTime, NPulsesProc, OperatingFreq)
Svarog = RadarObj(start_coords, RadarParams1, Signal1, start_time)



x0 = 50
y0 = 50
z0 = 50
Velocity = 300
phi_U = 45 #azimut
phi_V = 45 #elevation

periods_of_scanning = 10
t_btw_scanning = 0.1
for one_scan in range (1,periods_of_scanning+1):
    t = t_btw_scanning*(one_scan-1)
    x = x0 + Velocity*np.cos(math.radians(phi_V))*t
    y = y0 + Velocity*np.cos(math.radians(phi_V))*t
    z = z0 + Velocity*np.cos(math.radians(phi_U))*t
    # if (random.random() > 0.1): #c вероятностью 0.9 будет происходить обнаружение
    [r,u,v] = GRCStoUV([x,y,z])
    stdU = 0.07
    stdV = 0.07
    stdR = 20
    marochka = mark(u,v,r,stdU,stdV,stdR)
    Svarog.secondary_processing(marochka)

trajes = Svarog.Trajectories[0]
print(trajes.marks)