import math
import numpy as np
from project.modeling.ObjectModels.RadarObj import RadarObj,mark,radar_params,RectCS
from project.modeling.ObjectModels.CommandPostObj import CommandPostObj
from project.modeling.ObjectModels.SimpleTestPlane import SimpleTestPlane
from project.modeling.CSTransformator import GRCStoUV
from project.modeling.CSTransformator import UVtoGRCS
from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt


start_coords_radar_1 = RectCS(0, 0, 0)
start_time = 0
PRF = 10 ** 6
NPulsesProc = 1000
t_btw_scanning = NPulsesProc * (1/PRF)
Liqudator_Params_1 = radar_params(100000, 2, BW_U=1, BW_V=1, Scanning_V=[0, 60],
                            Tn=1000, PRF=PRF, SignalTime=10 ** (-6), NPulsesProc=NPulsesProc,
                            OperatingFreq=15 * 10 ** 9,
                            start_time=start_time, start_coords=start_coords_radar_1, SNRDetection=12)
Liqudator_Radar_1 = RadarObj(Liqudator_Params_1)


Supostat_1 = SimpleTestPlane(RectCS(0, 15000, 1000),RectCS(0, -200, 0),50)

overall_time = 200
time = np.linspace(0,overall_time,100)
x =[]
y=[]
z=[]
for t in time:
    # первичка
    measurements_from_1 = Liqudator_Radar_1.TrackingMeasure(Supostat_1,t)
    # if not measurements_from_1:
    #     pass
    # else:
    #     print(measurements_from_1)
    # вторичка
    # третичка
    x.append(measurements_from_1.X)
    y.append(measurements_from_1.Y)
    z.append(measurements_from_1.Z)
fig = plt.figure()
ax = plt.axes(projection ='3d')
x_rad = Liqudator_Radar_1.StartCoords.X
y_rad = Liqudator_Radar_1.StartCoords.Y
z_rad = Liqudator_Radar_1.StartCoords.Z
label = 'radar %d' % (Liqudator_Radar_1.Id)
ax.scatter(x_rad, y_rad, z_rad,color= 'blue')
ax.text(x_rad, y_rad, z_rad,label)
ax.plot3D(x, y, z,'blue')


# print(x)
# ax.legend(['1','2','3'])
plt.show()