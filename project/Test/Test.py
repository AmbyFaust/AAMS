import math
import numpy as np
from project.modeling.ObjectModels.RadarObj import RadarObj,mark,radar_params,RectCS
from project.modeling.ObjectModels.CommandPostObj import CommandPostObj
from project.modeling.ObjectModels.SimpleTestPlane import SimpleTestPlane
from project.modeling.CSTransformator import GRCStoUV
from project.modeling.CSTransformator import UVtoGRCS
from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt


start_coords_radar_1 = RectCS(0, -500, 0)
start_coords_radar_2 = RectCS(200, 200, 0)
start_coords_radar_3 = RectCS(-200, 500, 0)
start_time = 0
PRF = 10 ** 6
NPulsesProc = 1000
t_btw_scanning = NPulsesProc * (1/PRF)
Liqudator_Params_1 = radar_params(100000, 2, BW_U=3, BW_V=3, Scanning_V=[0, 60],
                            Tn=1000, PRF=PRF, SignalTime=10 ** (-6), NPulsesProc=NPulsesProc,
                            OperatingFreq=15 * 10 ** 9,
                            start_time=start_time, start_coords=start_coords_radar_1, SNRDetection=12)
Liqudator_Radar_1 = RadarObj(Liqudator_Params_1)
Liqudator_Params_2 = radar_params(1000000, 2, BW_U=3, BW_V=3, Scanning_V=[0, 60],
                            Tn=1000, PRF=PRF, SignalTime=10 ** (-6), NPulsesProc=NPulsesProc,
                            OperatingFreq=15 * 10 ** 9,
                            start_time=start_time, start_coords=start_coords_radar_2, SNRDetection=12)
Liqudator_Radar_2 = RadarObj(Liqudator_Params_2)
Liqudator_Params_3 = radar_params(1000000, 2, BW_U=3, BW_V=3, Scanning_V=[0, 60],
                            Tn=1000, PRF=PRF, SignalTime=10 ** (-6), NPulsesProc=NPulsesProc,
                            OperatingFreq=15 * 10 ** 9,
                            start_time=start_time, start_coords=start_coords_radar_3, SNRDetection=12)
Liqudator_Radar_3 = RadarObj(Liqudator_Params_3)

all_radars = [Liqudator_Radar_1, Liqudator_Radar_2,Liqudator_Radar_3]
Comman_Post_SKB_7 = CommandPostObj()



Supostat_1 = SimpleTestPlane(RectCS(4000, 400, 600),RectCS(20, 10, 0),50)
Supostat_2 = SimpleTestPlane(RectCS(8800, 1700, 300),RectCS(-10, -20, 0),70)
all_supostats = [Supostat_1, Supostat_2]

overall_time = 200
time = np.linspace(0,overall_time,int(overall_time/t_btw_scanning)+1)
for t in time:
    # первичка
    measurements_from_1 = Liqudator_Radar_1.MakeMeasurement(all_supostats,t)
    measurements_from_2 = Liqudator_Radar_2.MakeMeasurement(all_supostats,t)
    measurements_from_3 = Liqudator_Radar_3.MakeMeasurement(all_supostats,t)
    # if not measurements_from_1:
    #     pass
    # else:
    #     print(measurements_from_1)
    # вторичка
    Liqudator_Radar_1.secondary_processing(measurements_from_1)
    Liqudator_Radar_2.secondary_processing(measurements_from_2)
    Liqudator_Radar_3.secondary_processing(measurements_from_3)
    # третичка
    for one_radar in range(0,len(all_radars)):
        radar = all_radars[one_radar]
        all_radar_traj = radar.Trajectories
        # print(len(all_radar_traj))
        for one_traj in range(0, len(all_radar_traj)):
            current_traj = all_radar_traj[one_traj]
            if(current_traj.is_confimed == True):
                Comman_Post_SKB_7.tritial_processing(all_radars,current_traj)
fig = plt.figure()
ax = plt.axes(projection ='3d')
for radar in all_radars:
    x_rad = radar.StartCoords.X
    y_rad = radar.StartCoords.Y
    z_rad = radar.StartCoords.Z
    label = 'radar %d' % (radar.Id)
    if (radar.Id == 1):
        ax.scatter(x_rad, y_rad, z_rad,color= 'blue')
    if (radar.Id == 2):
        ax.scatter(x_rad, y_rad, z_rad,color= 'red')
    if (radar.Id == 3):
        ax.scatter(x_rad, y_rad, z_rad,color= 'green')
    ax.text(x_rad, y_rad, z_rad,label)

    all_radar_traj = radar.Trajectories
    for one_traj in range(0, len(all_radar_traj)):
        z = []
        x = []
        y = []
        current_traj = all_radar_traj[one_traj]
        xyz = current_traj.stack_of_coords
        [_, l, _] = xyz.shape
        for i in range(0, l):
            curr_xyz = xyz[:,i]
            x.append(curr_xyz[0])
            y.append(curr_xyz[1])
            z.append(curr_xyz[2])
        if (radar.Id == 1):
            ax.plot3D(x, y, z,'blue')
        if (radar.Id == 2):
            ax.plot3D(x, y, z,'red')
        if (radar.Id == 3):
            ax.plot3D(x, y, z,'green')

# print(x)
# ax.legend(['1','2','3'])
plt.show()