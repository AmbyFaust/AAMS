import math
import numpy as np
from project.modeling.ObjectModels.RadarObj import RadarObj,mark,radar_params,signal_params,RectCS
from project.modeling.ObjectModels.CommandPostObj import CommandPostObj
from project.modeling.CSTransformator import GRCStoUV
from project.modeling.CSTransformator import UVtoGRCS

start_time = 0
RadarParams1 = radar_params(1000, 2, BW_U=3, BW_V=3)
PRF = 10 ** 5
SignalTime = 10 ** (-6)
NPulsesProc = 1000
OperatingFreq = 15 * 10 ** 9
Signal1 = signal_params(PRF, SignalTime, NPulsesProc, OperatingFreq)
# свароги
Svarog_1 = RadarObj(RectCS(0, 0, 0), RadarParams1, Signal1, start_time,1)
Svarog_2 = RadarObj(RectCS(-200, 200, 10), RadarParams1, Signal1, start_time,2)
Svarog_3 = RadarObj(RectCS(20, 300, 5), RadarParams1, Signal1, start_time,3)

all_radars = [Svarog_1 , Svarog_2, Svarog_3]
Comman_Post_SKB_7 = CommandPostObj

# print(Svarog_2.StartCoords)
# print(Svarog_3.StartCoords)

x0 = 3000
y0 = 5000
z0 = 6000
Velocity = -300
phi_U = 45 #azimut
phi_V = 45 #elevation
target_id = 56

periods_of_scanning = 5
t_btw_scanning = 0.1

for one_scan in range(1, periods_of_scanning+1):
    t = t_btw_scanning*(one_scan-1)
    x = x0 + Velocity*np.cos(math.radians(phi_V))*t
    y = y0 + Velocity*np.cos(math.radians(phi_V))*t
    z = z0 + Velocity*np.cos(math.radians(phi_U))*t
    # if (random.random() > 0.1): #c вероятностью 0.9 будет происходить обнаружение
    [r,u,v] = GRCStoUV([x,y,z])
    stdU = 0.07
    stdV = 0.07
    stdR = 20
    marochka = mark(u,v,r,stdU,stdV,stdR,target_id)
    Svarog_1.secondary_processing(marochka)
    Svarog_2.secondary_processing(marochka)
    Svarog_3.secondary_processing(marochka)
    # for one_radar in range(0,1):
    #     radar = all_radars[one_radar]
    #     all_radar_traj = radar.Trajectories
    #     for one_traj in range(0, len(all_radar_traj)):
    #         current_traj = all_radar_traj[one_traj]
    #         print(current_traj.is_confimed)
    #         print('saad')
            # if(current_traj.is_confimed == True):
            #     print('ebash')
# trajes = Svarog_1.Trajectories[0]
# print(Svarog_1.Trajectories,Svarog_2.Trajectories)
# mark1 = mark(3,3,3,3,3,3,3)
# mark1 = mark1._replace(V=5)
# print(mark1)
