import math
import numpy as np
from project.modeling.ObjectModels.RadarObj import RadarObj,mark,radar_params,RectCS
from project.modeling.ObjectModels.CommandPostObj import CommandPostObj
from project.modeling.ObjectModels.SimpleTestPlane import SimpleTestPlane
from project.modeling.CSTransformator import GRCStoUV
from project.modeling.CSTransformator import UVtoGRCS

start_coords_radar_1 = RectCS(0, 0, 0)
start_coords_radar_2 = RectCS(200, 200, 0)
start_coords_radar_3 = RectCS(-200, 500, 0)
start_time = 0
PRF = 10 ** 6
NPulsesProc = 1000
t_btw_scanning = NPulsesProc * (1/PRF)
Liqudator_Params_1 = radar_params(1000, 2, BW_U=3, BW_V=3, Scanning_V=[0, 60],
                            Tn=1000, PRF=PRF, SignalTime=10 ** (-6), NPulsesProc=NPulsesProc,
                            OperatingFreq=15 * 10 ** 9,
                            start_time=start_time, start_coords=start_coords_radar_1, SNRDetection=12)
Liqudator_Radar_1 = RadarObj(Liqudator_Params_1)
Liqudator_Params_2 = radar_params(1000, 2, BW_U=3, BW_V=3, Scanning_V=[10, 70],
                            Tn=1000, PRF=PRF, SignalTime=10 ** (-6), NPulsesProc=NPulsesProc,
                            OperatingFreq=15 * 10 ** 9,
                            start_time=start_time, start_coords=start_coords_radar_2, SNRDetection=12)
Liqudator_Radar_2 = RadarObj(Liqudator_Params_2)
Liqudator_Params_3 = radar_params(1000, 2, BW_U=3, BW_V=3, Scanning_V=[10, 70],
                            Tn=1000, PRF=PRF, SignalTime=10 ** (-6), NPulsesProc=NPulsesProc,
                            OperatingFreq=15 * 10 ** 9,
                            start_time=start_time, start_coords=start_coords_radar_3, SNRDetection=12)
Liqudator_Radar_3 = RadarObj(Liqudator_Params_3)

all_radars = [Liqudator_Radar_1 , Liqudator_Radar_2, Liqudator_Radar_3]
Comman_Post_SKB_7 = CommandPostObj()

x0 = 3000
y0 = 5000
z0 = 6000
Velocity = -300
phi_U = 45 #azimut
phi_V = 45 #elevation

Supostat_1 = SimpleTestPlane(RectCS(4000, 400, 600),RectCS(20, 10, 0),50)
Supostat_2 = SimpleTestPlane(RectCS(1800, 3700, 300),RectCS(-3, 20, 0),50)
all_supostats = [Supostat_1,Supostat_2]

overall_time = 200
time = np.linspace(0,overall_time,int(overall_time/t_btw_scanning)+1)

for t in time:
    # print(t)
    # первичка
    measurements_from_1 = Liqudator_Radar_1.MakeMeasurement(all_supostats,t)
    # print (1,'  ',measurements_from_1)
    measurements_from_2 = Liqudator_Radar_2.MakeMeasurement(all_supostats,t)
    # print(2, '  ', measurements_from_2)
    measurements_from_3 = Liqudator_Radar_3.MakeMeasurement(all_supostats,t)
    # print(3, '  ', measurements_from_3)
    # вторичка
    Liqudator_Radar_1.secondary_processing(measurements_from_1)
    Liqudator_Radar_2.secondary_processing(measurements_from_2)
    Liqudator_Radar_3.secondary_processing(measurements_from_3)
    # третичка
    for one_radar in range(0,1):
        radar = all_radars[one_radar]
        all_radar_traj = radar.Trajectories
        for one_traj in range(0, len(all_radar_traj)):
            current_traj = all_radar_traj[one_traj]
            if(current_traj.is_confimed == True):
                Comman_Post_SKB_7.tritial_processing(all_radars,current_traj)
