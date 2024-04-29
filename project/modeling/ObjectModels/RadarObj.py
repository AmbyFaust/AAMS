from project.modeling.ObjectModels.DataStructures import radar_params, UVCS, RectCS, mark,trajectory
import math
import numpy as np
from project.modeling.ObjectModels.Object import Object
import matplotlib.pyplot as plt
from project.modeling.CSTransformator import GRCStoUV, UVtoLRCS
from project.modeling.CSTransformator import UVtoGRCS



# Класс Радар
class RadarObj(Object):
    Trajectories = []
    ObjectName = 'Radar'
    Id = 1

    # Конструктор Класса
    def __init__(self, radar_params):
        self.Id = RadarObj.Id
        RadarObj.Id += 1
        self.Trajectories = []
        self.StartCoords = radar_params.start_coords
        self.ObjCoords = radar_params.start_coords
        self.StartTime = radar_params.start_time
        self.RadarParams = radar_params
        self.UBeam = 0
        self.VBeam = 0
        self.wavelength = 3 * 10 ** 8 / radar_params.OperatingFreq
        self.RangeResolution = 3 * 10 ** 8 * radar_params.SignalTime / 2
        self.NoisePower = 1.38 * 10 ** (-23) * radar_params.Tn / radar_params.SignalTime
        self.t_btw_transmiting = radar_params.Tn * (1/radar_params.PRF)
        self.Measurement = 0

        # Функция изменения углов сканирования

    def ChangeAnglOfViev(self, UBeam, VBeam):
        self.UBeam = UBeam
        self.VBeam = VBeam
        # Функция для расчёта ОСШ

    def CalculateSNR(self, TargetRange, TargetRCS):
        SNR = self.RadarParams.EIRP * self.RadarParams.Seff * TargetRCS / (
                (4 * math.pi) ** 2 * TargetRange ** 4 * self.NoisePower)
        return SNR

    # Функция для расчёта координат целей с ошибками(имитируем измерение)
    def CalcMistake(self, target_coordsSpH, SNR,targid):
        stdU = self.RadarParams.BW_U / (2 * SNR) ** (1 / 2)
        stdV = self.RadarParams.BW_V / (2 * SNR) ** (1 / 2)
        stdR = self.RangeResolution / (2 * SNR) ** (1 / 2)
        Umeasured = np.random.normal(target_coordsSpH.U, stdU, 1)
        Vmeasured = np.random.normal(target_coordsSpH.V, stdV, 1)
        Rmeasured = np.random.normal(target_coordsSpH.R, stdR, 1)
        return mark(U=Umeasured, V=Vmeasured, R=Rmeasured, stdU=stdU, stdV=stdV, stdR=stdR, TargetId=targid)

    def MakeMeasurement(self, targets, time):
        BeamCoords = self.scanning_procces(time)
        # print('Направление луча:',BeamCoords)
        marks = []
        for target in targets:
            targetInfo = target.ReturnPlaneInformation(time)
            targetCoordsUV = GRCStoUV(targetInfo.coordinates, self.ObjCoords)
            # print('Положение цели',targetInfo.TargetId,':', targetCoordsUV)
            # print('Положение луча', BeamCoords)
            # print(targetCoordsUV)
            if abs(BeamCoords[0]-targetCoordsUV.U) <self.RadarParams.BW_U/2 and abs(BeamCoords[1]-targetCoordsUV.V) <self.RadarParams.BW_V/2:
                TargetSNR = self.CalculateSNR(targetCoordsUV.R, targetInfo.RCS)
                # print('ОСШ от цели',targetInfo.TargetId,TargetSNR)
                if TargetSNR > self.RadarParams.SNRDetection:
                    print('TargetDetected')
                    mark = self.CalcMistake(targetCoordsUV,TargetSNR,targetInfo.TargetId)
                    print('Истинные координаты цели ', targetInfo.coordinates)
                    print('Истинные координаты цели переведены обратно ', UVtoGRCS(targetCoordsUV, self.StartCoords))
                    print('Измеренные координаты цели ', UVtoGRCS(UVCS(mark.U, mark.V, mark.R), self.StartCoords))
                    marks.append(mark)

        # self.Measurement += 1
        return marks

    def scanning_procces(self,t):
        # t кратен времени между зондированиями
        # t характеризует номер зондирования конкретного радара, при t = 0 положение луча на
        [Vmin, Vmax] = self.RadarParams.Scanning_V
        # print(Vmax)
        N = t / self.t_btw_transmiting
        # print(N)
        N_V = (Vmax - Vmin) / self.RadarParams.BW_V
        # print(N_V)
        N_U = 360 / self.RadarParams.BW_U
        # print(N_U)
        N_of_one_per = N_V * N_U
        # print(N_of_one_per)
        N_in_scan = N - (N // N_of_one_per) * N_of_one_per
        # print(N_in_scan)
        N_V_in_scan = N_in_scan % (N_V)
        # print(N_V_in_scan)
        N_U_in_scan = N_in_scan // (N_V)
        # print(N_U_in_scan)
        Current_V = Vmin + (self.RadarParams.BW_V / 2) + self.RadarParams.BW_V*(N_V_in_scan)
        Current_U = -180 + (self.RadarParams.BW_U / 2) + self.RadarParams.BW_U*(N_U_in_scan)
        return [Current_U, Current_V]

    def secondary_processing(self, marks):
        for mark in marks:
            u = mark[0]
            v = mark[1]
            r = mark[2]
            xyz = UVtoGRCS(UVCS(r,u,v),self.StartCoords)
            x = xyz.X
            y = xyz.Y
            z = xyz.Z

            # print(u, v, r)
            targ_id = mark[6]
            if not self.Trajectories:
                self.intitiate_traj(targ_id, x, y, z)

            else:
                key = 0
                for one_traj in range(1, len(self.Trajectories) + 1):
                    current_traj = self.Trajectories[one_traj - 1]
                    if (current_traj.target_id == targ_id):
                        key = 1
                        curr_traj_marks = current_traj.stack_of_coords
                        curr_coord = np.array([[x], [y], [z]])
                        # print(self.Trajectories[one_traj - 1].stack_of_coords)
                        self.Trajectories[one_traj - 1] = current_traj._replace(stack_of_coords = np.concatenate((curr_traj_marks, curr_coord), axis=1))
                        if (current_traj.is_confimed == False):
                            self.check_if_its_supostat(one_traj)
                if key == 0:
                    self.intitiate_traj(targ_id, x, y, z)

    def intitiate_traj (self,target_id, x, y, z):
        initiation_traj = trajectory(np.array([[x], [y], [z]]),target_id,False)
        self.Trajectories.append(initiation_traj)
    def check_if_its_supostat (self,one_traj):
        current_traj = self.Trajectories[one_traj-1]
        # print(current_traj.stack_of_coords.shape)
        [_, l,_] = current_traj.stack_of_coords.shape
        if (l == 5):
            self.Trajectories[one_traj - 1] = current_traj._replace(is_confimed = True)
            print ('Supostat with id',current_traj.target_id,' is detected by locator with id',self.Id)


if __name__ == "__main__":
    start_coords = RectCS(0, 0, 0)
    start_time = 0
    RadarParams1 = radar_params(1000, 2, BW_U=3, BW_V=3, Scanning_V=[10, 70],
                                Tn=1000, PRF=10 ** 5, SignalTime=10 ** (-6), NPulsesProc=1000,
                                OperatingFreq=15 * 10 ** 9,
                                start_time=start_time, start_coords=start_coords, SNRDetection=12)
    Radar1 = RadarObj(RadarParams1)
    # Radar1 = RadarObj()
    Radar1.ChangeAnglOfViev(1, 1)
    targetcoords1 = [RectCS(10, 10, 5)]
    # targetcoords1New = GRCStoLRCS(targetcoords1)
    SNR = Radar1.CalculateSNR(1000, 10)
    overall_time = 20
    t_btw_scanning = 1000 * (1 / 10 ** 5)
    time = np.linspace(0,overall_time,int(overall_time/t_btw_scanning)+1)
    x = []
    y = []
    for point in time:
        vievpoint = Radar1.scanning_procces(point)
        x.append(vievpoint[0])
        y.append(vievpoint[1])
    # print(Radar1.UBeam, Radar1.UBeam)
    plt.plot(x,y)
    plt.show()

