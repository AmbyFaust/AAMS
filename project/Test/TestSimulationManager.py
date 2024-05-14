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
start_coords_radar_1 = {'x':0,'y': -500,'z':0}
start_coords_radar_2 = {'x':200,'y': 200,'z':0}
start_coords_radar_3 = {'x':-200,'y': 500,'z':0}

start_time = 0
PRF = 10 ** 5
NPulsesProc = 1000
t_btw_scanning = NPulsesProc * (1/PRF)
Liqudator_Params_1 = radar_params(100000, 2, BW_U=3, BW_V=3, Scanning_V=[0, 60],
                            Tn=1000, PRF=PRF, SignalTime=10 ** (-6), NPulsesProc=NPulsesProc,
                            OperatingFreq=15 * 10 ** 9,
                            start_time=start_time, start_coords=start_coords_radar_1, SNRDetection=12)
Liqudator_Radar_1 = RadarObj(Liqudator_Params_1)
Launcher_1 = LaunchSystem(start_coords_radar_1['x'],start_coords_radar_1['y'],start_coords_radar_1['z'])
Launcher_1.radarId = Liqudator_Radar_1.Id

Liqudator_Params_2 = radar_params(1000000, 2, BW_U=3, BW_V=3, Scanning_V=[0, 60],
                            Tn=1000, PRF=PRF, SignalTime=10 ** (-6), NPulsesProc=NPulsesProc,
                            OperatingFreq=15 * 10 ** 9,
                            start_time=start_time, start_coords=start_coords_radar_2, SNRDetection=12)
Liqudator_Radar_2 = RadarObj(Liqudator_Params_2)
Launcher_2 = LaunchSystem(start_coords_radar_2['x'],start_coords_radar_2['y'],start_coords_radar_2['z'])
Launcher_2.radarId = Liqudator_Radar_2.Id

Liqudator_Params_3 = radar_params(1000000, 2, BW_U=3, BW_V=3, Scanning_V=[0, 60],
                            Tn=1000, PRF=PRF, SignalTime=10 ** (-6), NPulsesProc=NPulsesProc,
                            OperatingFreq=15 * 10 ** 9,
                            start_time=start_time, start_coords=start_coords_radar_3, SNRDetection=12)
Liqudator_Radar_3 = RadarObj(Liqudator_Params_3)
Launcher_3 = LaunchSystem(start_coords_radar_3['x'],start_coords_radar_3['y'],start_coords_radar_3['z'])
Launcher_3.radarId = Liqudator_Radar_3.Id

all_radars = [Liqudator_Radar_1, Liqudator_Radar_2,Liqudator_Radar_3]
Comman_Post_SKB_7 = CommandPostObj()

point1 = {'x':30000,'y':0,'z':1000}
point2 = {'x':25000,'y':5000,'z':1000}
point3 = {'x':100000,'y':5000,'z':1000}
point4 = {'x':5000,'y':10000,'z':1000}
control_points = [point1,point2,point3,point4]
target = Target("jet", "F-15", 1, 400, control_points)

SM.radars[Liqudator_Radar_1.Id]=Liqudator_Radar_1
SM.radars[Liqudator_Radar_2.Id]=Liqudator_Radar_2
SM.radars[Liqudator_Radar_3.Id]=Liqudator_Radar_3
SM.targets[target.Id]=target
SM.launchers[Launcher_1.Id]=Launcher_1
SM.launchers[Launcher_2.Id]=Launcher_2
SM.launchers[Launcher_3.Id]=Launcher_3

SM.modeling()