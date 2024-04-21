from collections import namedtuple
import math
import numpy as np
from project.modeling.ObjectModels.Object import Object

from project.modeling.CSTransformator import GRCStoUV
from project.modeling.CSTransformator import UVtoGRCS

# объявляем используемые типы данных
radar_params = namedtuple('radar_params', 'EIRP Seff  BW_U BW_V')
signal_params = namedtuple('signal_params', 'PRF SignalTime NPulsesProc OperatingFreq')
mark = namedtuple('mark', 'U V R stdU stdV stdR target_id')
trajectory = namedtuple('trajectory', 'stack_of_coords target_id is_confimed')
target_params = namedtuple('target_params', 'RCS coordinates')
RectCS = namedtuple('RectCS', 'X Y Z')
UVCS = ('UVCS', 'U V R')


# Класс Радар
class RadarObj(Object):

    # Конструктор Класса
    def __init__(self, start_coords, radar_params, signal_params, start_time, radar_id):
        self.Trajectories = []
        self.RadarID = radar_id
        self.StartCoords = start_coords
        self.RadarParams = radar_params
        self.SignalParams = signal_params
        self.StartTime = start_time
        self.UBeam = 0
        self.VBeam = 0
        self.wavelength = 3 * 10 ** 8 / signal_params.OperatingFreq
        self.RangeResolution = 3 * 10 ** 8 * signal_params.SignalTime / 2
        self.t_btw_transmiting = signal_params.NPulsesProc/signal_params.PRF
        # Функция изменения углов сканирования

    def ChangeAnglOfViev(self, UBeam, VBeam):
        self.UBeam = UBeam
        self.VBeam = VBeam
        # Функция для расчёта ОСШ

    def CalculateSNR(self, TargetRange, TargetRCS):
        SNR = self.RadarParams.EIRP * self.RadarParams.Seff * TargetRCS / ((4 * math.pi) ** 2 * TargetRange ** 4)
        return SNR

    # Функция для расчёта координат целей с ошибками(имитируем измерение)
    def CalcMistake(self, target_coordsUV, SNR):
        stdU = self.RadarParams.BW_U / (2 * SNR) ** (1 / 2)
        stdV = self.RadarParams.BW_V / (2 * SNR) ** (1 / 2)
        stdR = self.RangeResolution / (2 * SNR) ** (1 / 2)
        Umeasured = np.random.normal(target_coordsUV.U, stdU, 1)
        Vmeasured = np.random.normal(target_coordsUV.V, stdV, 1)
        Rmeasured = np.random.normal(target_coordsUV.R, stdR, 1)
        return mark(U=Umeasured, V=Vmeasured, R=Rmeasured, stdU=stdU, stdV=stdV, stdR=stdR)

    def GRCStoLRCS(self, targets_coordsGRCS):
        targets_coordsLRCS = [None] * len(targets_coordsGRCS)

        for i in range(len(targets_coordsGRCS)):
            print(targets_coordsGRCS[i])
            targets_coordsLRCS[i] = RectCS(X=(targets_coordsGRCS[i].X - self.StartCoords.X),
                                           Y=targets_coordsGRCS[i].Y - self.StartCoords.Y,
                                           Z=targets_coordsGRCS[i].Z - self.StartCoords.Z)
        return targets_coordsLRCS



    def secondary_processing(self, mark):

        u = mark[0]
        v = mark[1]
        r = mark[2]
        targ_id = mark[6]
        # trafectories = self.Trajectories  # get all trajes
        if not self.Trajectories:
            self.intitiate_traj(targ_id, r, u, v)
        else:
            key = 0
            for one_traj in range(1, len(self.Trajectories) + 1):
                current_traj = self.Trajectories[one_traj - 1]
                # print(current_traj.is_confimed)

                if (current_traj.target_id == targ_id):
                    key = 1
                    curr_traj_marks = current_traj.stack_of_coords
                    curr_coord = np.array([[r], [u], [v]])
                    # print(self.Trajectories[one_traj - 1].stack_of_coords)
                    self.Trajectories[one_traj - 1] = current_traj._replace(stack_of_coords = np.concatenate((curr_traj_marks, curr_coord), axis=1))

                    if (current_traj.is_confimed == False):
                        self.check_if_its_supostat(one_traj)
            if key == 0:
                self.intitiate_traj(targ_id, r, u, v)
    def intitiate_traj (self,target_id, r, u, v):
        initiation_traj = trajectory(np.array([[r], [u], [v]]),target_id,False)
        self.Trajectories.append(initiation_traj)
    def check_if_its_supostat (self,one_traj):
        current_traj = self.Trajectories[one_traj-1]
        [_, l] = current_traj.stack_of_coords.shape
        if (l == 5):
            self.Trajectories[one_traj - 1] = current_traj._replace(is_confimed = True)
            print ('Supostat with id',current_traj.target_id,' is detected by locator with id',self.RadarID)


if __name__ == "__main__":
    start_coords = RectCS(0, 0, 0)
    start_time = 0
    RadarParams1 = radar_params(1000, 2, BW_U=3, BW_V=3)
    Signal1 = signal_params(10 ** 3, 10 ** (-6), 1000, 15 * 10 ** 9)
    radar_id = 100
    Radar1 = RadarObj(start_coords, RadarParams1, Signal1, start_time, radar_id)
    # Radar1 = RadarObj()
    Radar1.ChangeAnglOfViev(1, 1)
    targetcoords1 = [RectCS(10, 10, 5)]
    targetcoords1New = Radar1.GRCStoLRCS(targetcoords1)
    print(Radar1.UBeam, Radar1.UBeam)
