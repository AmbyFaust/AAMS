from project.modeling.SimulationManager import SimulationManager
import math
import numpy as np
from project.modeling.ObjectModels.RadarObj import RadarObj,mark,radar_params,RectCS
from project.modeling.ObjectModels.CommandPostObj import CommandPostObj
from project.modeling.ObjectModels.SimpleTestPlane import SimpleTestPlane
from project.modeling.CSTransformator import GRCStoUV
from project.modeling.CSTransformator import UVtoGRCS
from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt
from project.modeling.ObjectModels.Launcher_and_missile import LaunchSystem
from project.modeling.ObjectModels.TargetObj import Target
SM = SimulationManager("SimulationConfig")

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
Launcher_1 = LaunchSystem(start_coords_radar_1.X,start_coords_radar_1.Y,start_coords_radar_1.Z)
Launcher_1.radarId = Liqudator_Radar_1.Id

Liqudator_Params_2 = radar_params(1000000, 2, BW_U=3, BW_V=3, Scanning_V=[0, 60],
                            Tn=1000, PRF=PRF, SignalTime=10 ** (-6), NPulsesProc=NPulsesProc,
                            OperatingFreq=15 * 10 ** 9,
                            start_time=start_time, start_coords=start_coords_radar_2, SNRDetection=12)
Liqudator_Radar_2 = RadarObj(Liqudator_Params_2)
Launcher_2 = LaunchSystem(start_coords_radar_2.X,start_coords_radar_2.Y,start_coords_radar_2.Z)
Launcher_2.radarId = Liqudator_Radar_2.Id

Liqudator_Params_3 = radar_params(1000000, 2, BW_U=3, BW_V=3, Scanning_V=[0, 60],
                            Tn=1000, PRF=PRF, SignalTime=10 ** (-6), NPulsesProc=NPulsesProc,
                            OperatingFreq=15 * 10 ** 9,
                            start_time=start_time, start_coords=start_coords_radar_3, SNRDetection=12)
Liqudator_Radar_3 = RadarObj(Liqudator_Params_3)
Launcher_3 = LaunchSystem(start_coords_radar_3.X,start_coords_radar_3.Y,start_coords_radar_3.Z)
Launcher_3.radarId = Liqudator_Radar_3.Id

all_radars = [Liqudator_Radar_1, Liqudator_Radar_2,Liqudator_Radar_3]
Comman_Post_SKB_7 = CommandPostObj()

control_points = [
    (30000, 0, 100),
    (25000, 5000, 100),
    (100000, 5000, 100),
    (5000, 10000, 100)
]
target = Target("jet", "F-15", 1, 400, control_points)

SM.radars.append(Liqudator_Radar_1)
SM.radars.append(Liqudator_Radar_2)
SM.radars.append(Liqudator_Radar_3)

SM.targets.append(target)

SM.launchers.append(Launcher_1)
SM.launchers.append(Launcher_2)
SM.launchers.append(Launcher_1)

SM.modeling()