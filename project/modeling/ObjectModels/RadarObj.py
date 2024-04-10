from collections import namedtuple
import math
import numpy as np
from Object import Object

# объявляем используемые типы данных
radar_params = namedtuple('radar_params', 'EIRP Seff BW_U BW_V')
signal_params = namedtuple('signal_params', 'PRF SignalTime NPulsesProc OperatingFreq')
mark = namedtuple('mark', 'U V R stdU stdV stdR')
target_params = namedtuple('target_params', 'RCS coordinates')
RectCS = namedtuple('RectCS', 'X Y Z')
UVCS = ('UVCS', 'U V R')


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


if __name__ == "__main__":
    start_coords = RectCS(0, 0, 0)
    start_time = 0
    RadarParams1 = radar_params(1000, 2, BW_U=0.1, BW_V=0.1)
    Signal1 = signal_params(10 ^ -3, 10 ^ -6, 1000, 15 * 10 ** 9)
    Radar1 = RadarObj(start_coords, RadarParams1, Signal1, start_time)
    # Radar1 = RadarObj()
    Radar1.ChangeAnglOfViev(1, 1)
    targetcoords1 = [RectCS(10, 10, 5)]
    targetcoords1New = Radar1.GRCStoLRCS(targetcoords1)
    print(Radar1.UBeam, Radar1.UBeam)
