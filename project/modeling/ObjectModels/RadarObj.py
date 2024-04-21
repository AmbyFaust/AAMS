from project.modeling.ObjectModels.DataStructures import radar_params, signal_params, UVCS, RectCS, mark
import math
import numpy as np
from project.modeling.ObjectModels.Object import Object

from project.modeling.CSTransformator import GRCStoUV
from project.modeling.CSTransformator import UVtoGRCS


# Класс Ветка
class brunch(Object):
    marks = np.array([])
    next_gate = []
    initiated = True


# Класс Радар
class RadarObj(Object):
    Trajectories = []

    # Конструктор Класса
    def __init__(self, start_coords, radar_params, signal_params, start_time):
        self.StartCoords = start_coords
        self.RadarParams = radar_params
        self.SignalParams = signal_params
        self.StartTime = start_time
        self.UBeam = 0
        self.VBeam = 0
        self.wavelength = 3 * 10 ** 8 / signal_params.OperatingFreq
        self.RangeResolution = 3 * 10 ** 8 * signal_params.SignalTime / 2
        self.NoisePower = 1.38 * 10 ** (-23) * radar_params.Tn / signal_params.SignalTime
        self.t_btw_transmiting = signal_params.NPulsesProc / signal_params.PRF

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

    def scanning_procces(self, t):
        # t кратен времени между зондированиями
        # t характеризует номер зондирования конкретного радара, при t = 0 положение луча на
        [Vmin, Vmax] = self.RadarParams.Scanning_V
        N = t / self.t_btw_transmiting
        N_V = (Vmax - Vmin) / self.RadarParams.BW_V
        N_U = 360 / self.RadarParams.BW_U
        N_of_one_per = N_V * N_U
        N_in_scan = N - (N // N_of_one_per) * N_of_one_per
        N_V_in_scan = N_in_scan % (N_V)
        N_U_in_scan = N_in_scan // (N_V)
        Current_V = Vmin + (self.RadarParams.BW_V / 2) * (1 + N_V_in_scan)
        Current_U = (self.RadarParams.BW_U / 2) * (1 + N_U_in_scan)
        return [Current_U, Current_V]

    def secondary_processing(self, mark):
        u = mark[0]
        v = mark[1]
        r = mark[2]
        stdU = mark[3]
        stdV = mark[4]
        stdR = mark[5]
        [x, y, z] = UVtoGRCS([r, u, v])

        trafectories = self.Trajectories  # get all trajes

        if not trafectories:
            self.intitiate_traj(x, y, z, r, u, v)
        else:
            for one_traj in range(1, len(trafectories) + 1):
                current_traj = trafectories[one_traj - 1]
                if (current_traj.initiated == True):
                    gates = current_traj.next_gate
                    if (x > gates[0] and x < gates[1] and y > gates[2] and y < gates[3] and z > gates[4] and z < gates[
                        5]):
                        curr_traj_marks = current_traj.marks
                        curr_coord = np.array([[r], [u], [v]])
                        current_traj.marks = np.concatenate((curr_traj_marks, curr_coord), axis=1)
                        current_traj.next_gate = self.get_tracking_gate(current_traj.marks, stdU, stdV, stdR)
                        current_traj.initiated = False
                else:
                    gates = current_traj.next_gate
                    if (r > gates[0] and r < gates[1] and u > gates[2] and u < gates[3] and v > gates[4] and v < gates[
                        5]):
                        curr_traj_marks = current_traj.marks
                        curr_coord = np.array([[r], [u], [v]])
                        current_traj.marks = np.concatenate((curr_traj_marks, curr_coord), axis=1)
                        current_traj.next_gate = self.get_tracking_gate(current_traj.marks, stdU, stdV, stdR)

    def intitiate_traj(self, x, y, z, r, u, v):
        creating_brunch = brunch
        creating_brunch.marks = np.array([[r], [u], [v]])
        creating_brunch.next_gate = self.get_initation_gate(x, y, z)
        creating_brunch.initiated = True
        RadarObj.Trajectories.append(creating_brunch)

    def get_initation_gate(self, x, y, z):
        initation_radius = self.t_btw_transmiting * 500
        return [x - initation_radius, x + initation_radius, y - initation_radius, y + initation_radius,
                z - initation_radius, z + initation_radius]

    def get_tracking_gate(self, marks, stdU, stdV, stdR):
        prev_mark = marks[0:3, -2]
        last_mark = marks[0:3, -1]
        last_mark = UVtoGRCS(last_mark)
        prev_mark = UVtoGRCS(prev_mark)
        V_x = last_mark[0] - prev_mark[0]
        V_y = last_mark[1] - prev_mark[1]
        V_z = last_mark[2] - prev_mark[2]
        extr_x = last_mark[0] + V_x
        extr_y = last_mark[1] + V_y
        extr_z = last_mark[2] + V_z
        [r_extr, u_extr, v_extr] = GRCStoUV([extr_x, extr_y, extr_z])
        r1 = r_extr - 3 * stdR
        r2 = r_extr + 3 * stdR
        u1 = u_extr - 3 * stdU
        u2 = u_extr + 3 * stdU
        v1 = v_extr - 3 * stdV
        v2 = v_extr + 3 * stdV
        return [r1, r2, u1, u2, v1, v2]


if __name__ == "__main__":
    start_coords = RectCS(0, 0, 0)
    start_time = 0
    RadarParams1 = radar_params(1000, 2, BW_U=3, BW_V=3, Scanning_V=[10, 70], Tn=1000)
    Signal1 = signal_params(10 ** 3, 10 ** (-6), 1000, 15 * 10 ** 9)
    Radar1 = RadarObj(start_coords, RadarParams1, Signal1, start_time)
    # Radar1 = RadarObj()
    Radar1.ChangeAnglOfViev(1, 1)
    targetcoords1 = [RectCS(10, 10, 5)]
    targetcoords1New = Radar1.GRCStoLRCS(targetcoords1)
    SNR = Radar1.CalculateSNR(1000, 10)
    CoordsWithMis
    print(SNR)
    # print(Radar1.UBeam, Radar1.UBeam)
