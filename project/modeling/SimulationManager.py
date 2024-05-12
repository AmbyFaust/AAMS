import os
import json
import pandas as pd

from .ObjectModels.DataStructures import radar_params
from .ObjectModels.RadarObj import RadarObj
from .ObjectModels.TargetObj import Target
from .ObjectModels.Launcher_and_missile import LaunchSystem
from project.modeling.ObjectModels.CommandPostObj import CommandPostObj


class SimulationManager:
    def __init__(self, path):
        self.path = path

        self.radars = dict()
        self.targets = dict()
        self.launchers = dict()
        self.__load_objects()

        self.rockets = []
        self.CurrModelingTime = 0
        self.TimeStep = 10**-1
        self.endTime = 1000
        self.CommPost = CommandPostObj()

        self.data = pd.DataFrame(columns=['object_type', 'object_id', 'time', 'x', 'y', 'z'])

    def __load_objects(self):
        with open(self.path, 'r') as file:
            d = json.load(file)

            for radar_data in d['radars']:
                self.__load_radar_object(radar_data)
                self.__load_launcher_object(radar_data)

            for target_data in d['targets']:
                self.__load_target_object(target_data)

    def modeling(self):
        while self.CurrModelingTime < self.endTime:
            self.modeling_step()

        self.data.to_csv(os.path.dirname(self.path) + '/data.csv')

    def modeling_step(self):
        # Изменяем текущее время модели
        self.CurrModelingTime += self.TimeStep
        if self.CurrModelingTime > 3:
            print("Время моделирования:", self.CurrModelingTime)

        for target_id, target in self.targets.items():
            print(target.CurrCoords)

        # Моделируем ПОИ и ВОИ(первичка и вторичка)
        for radar_id, radar in self.radars.items():
            measurements_from_radar = radar.MakeMeasurement(self.targets.values(), self.CurrModelingTime)
            radar.secondary_processing(measurements_from_radar)

        # Моделируем ТОИ(третичка)
        for radar_id, radar in self.radars.items():
            all_radar_traj = radar.Trajectories
            for current_traj in all_radar_traj:
                if current_traj.is_confimed:
                    self.rockets.append(
                        self.CommPost.tritial_processing(
                            self.radars.values(),
                            current_traj,
                            self.launchers.values(),
                            self.CurrModelingTime)
                    )

        # Сдвигаем все объекты(цели и ракеты) в соответствии с текущим временем (Если они в состоянии IsLive)
        for rocket in self.rockets:
            rocket.move(self.CurrModelingTime)
        for target_id, target in self.targets.items():
            if target.Islive:
                target.move(self.CurrModelingTime)

        # Проверяем условия подрыва и выдаём координаты цели для полёта ракеты  (если есть ракеты)
        for rocket in self.rockets:
            # Проверяем условия подрыва и в случае подрыва задаём всем объектам флаг (IsLive = false)
            rocket.checkDetonationConditions(self.targets.values())
            #Ракета должна знать к кому радару она относится и какой цели летит
            targetCoord = self.radars[rocket.radarId].TrackingMeasure(
                self.targets[rocket.targetId],
                self.CurrModelingTime
            )
            rocket.changeDirectionofFlight(targetCoord)

    def __load_radar_object(self, radar_data):
        self.radars[radar_data['id']] = RadarObj(radar_params(
            EIRP=radar_data['eirp'],
            Seff=radar_data['seff'],
            BW_U=radar_data['bw_u'],
            BW_V=radar_data['bw_v'],
            Scanning_V=radar_data['scanning_v'],
            Tn=radar_data['t_n'],
            PRF=radar_data['prf'],
            SignalTime=radar_data['signal_time'],
            NPulsesProc=radar_data['n_pulses_proc'],
            OperatingFreq=radar_data['operating_freq'],
            start_time=radar_data['start_time'],
            start_coords=radar_data['start_coordinates'],
            SNRDetection=radar_data['snr_detection']
        ), radar_id=radar_data['id'])

    def __load_target_object(self, target_data):
        self.targets[target_data['id']] = Target(
            type=target_data['type'],
            ObjectName='{}_{}'.format(target_data['type'], target_data['id']),
            epr=target_data['epr'],
            velocity=target_data['speed'],
            control_points=target_data['coordinates'],
            target_id=target_data['id']
        )

    def __load_launcher_object(self, launcher_data):
        self.launchers[launcher_data['id']] = LaunchSystem(
            x=launcher_data['start_coordinates']['x'],
            y=launcher_data['start_coordinates']['y'],
            z=launcher_data['start_coordinates']['x'],
            launcher_id=launcher_data['id']
        )


if __name__ == "__main__":
    sm = SimulationManager('../../results/objects.json')
    sm.modeling()
