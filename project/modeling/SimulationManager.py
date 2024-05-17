import os
import json
import pandas as pd
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QProgressDialog, QMessageBox

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
        self.TimeStep = 10 ** -2
        self.endTime = 1000
        self.CommPost = CommandPostObj()

        self.data = pd.DataFrame(columns=['object_type', 'object_id', 'time', 'x', 'y', 'z'])

    def __load_objects(self):
        with open(self.path, 'r', encoding='utf-8') as file:
            d = json.load(file)

            for radar_data in d['objects']['radars']:
                self.__load_radar_object(radar_data)
                self.__load_launcher_object(radar_data)

            for target_data in d['objects']['targets']:
                self.__load_target_object(target_data)

    def modeling(self):
        if len(self.radars) > 0:
            self.TimeStep = min([r.RadarParams.NPulsesProc / r.RadarParams.PRF for r in self.radars.values()])
        targetWayTime = []
        for target in self.targets.values():
            endTargetTime = target.get_last_time_target()
            targetWayTime.append(endTargetTime)
        self.endTime = min(targetWayTime) - self.TimeStep

        progress_dialog = QProgressDialog("Моделирование в процессе...", None, 0, 100)
        progress_dialog.setWindowModality(Qt.WindowModal)
        progress_dialog.setMinimumDuration(0)
        progress_dialog.setCancelButton(None)
        progress_dialog.show()

        while self.CurrModelingTime < self.endTime:
            if self.__checkTargetsLifeStatus():
                self.modeling_step()
            else:
                break

            progress_value = int((self.CurrModelingTime / self.endTime) * 100)
            progress_dialog.setValue(progress_value)

        progress_dialog.close()

        self.data.to_csv(os.path.dirname(self.path) + '/data.csv')

        msg_modeling = QMessageBox()
        msg_modeling.setIcon(QMessageBox.Information)
        msg_modeling.setText("Расчет выполнен. Нажмите ОК.")
        msg_modeling.setWindowTitle("Информация")
        msg_modeling.exec()

    def modeling_step(self):
        # Изменяем текущее время модели
        self.CurrModelingTime = round(self.CurrModelingTime + self.TimeStep,4)
        # print("Время моделирования:", self.CurrModelingTime)

        # Моделируем ПОИ и ВОИ(первичка и вторичка)
        for radar_id, radar in self.radars.items():
            measurements_from_radar = radar.MakeMeasurement(self.targets.values(), self.CurrModelingTime)
            if (len(measurements_from_radar)>0):
                # print(self.CurrModelingTime," time and radar id", radar_id)
                radar.secondary_processing(measurements_from_radar)


        # Моделируем ТОИ(третичка)
        for radar_id, radar in self.radars.items():
            all_radar_traj = radar.Trajectories
            for current_traj in all_radar_traj:
                if current_traj.is_confimed:
                    rocket = self.CommPost.tritial_processing(
                        self.radars,
                        current_traj,
                        self.launchers.values(),
                        self.CurrModelingTime)
                    if rocket is not None:
                        self.rockets.append(rocket)

        # Сдвигаем все объекты(цели и ракеты) в соответствии с текущим временем (Если они в состоянии IsLive)
        for rocket in self.rockets:
            rocket.move(self.CurrModelingTime)
        for target_id, target in self.targets.items():
            if target.Islive:
                target.move(self.CurrModelingTime)

        # Проверяем условия подрыва и выдаём координаты цели для полёта ракеты  (если есть ракеты)
        for rocket in self.rockets:
            # Проверяем условия подрыва и в случае подрыва задаём всем объектам флаг (IsLive = false)
            if rocket.Islive:
                rocket.checkDetonationConditions(self.targets.values())
                # Ракета должна знать к кому радару она относится и какой цели летит
                targetCoord = self.radars[rocket.radarId].TrackingMeasure(
                    self.targets[rocket.targetId],
                    self.CurrModelingTime
                )
                rocket.changeDirectionofFlight(targetCoord)

        # print('Targets')
        for target_id, target in self.targets.items():
            # print(target.CurrCoords)
            self.data.loc[len(self.data)] = {
                'object_type': 'target',
                'object_id': target_id,
                'time': self.CurrModelingTime,
                'x': target.CurrCoords.X,
                'y': target.CurrCoords.Y,
                'z': target.CurrCoords.Z,
            }
        # print('Rockets')
        for rocket in self.rockets:
            self.data.loc[len(self.data)] = {
                'object_type': 'rocket',
                'object_id': rocket.id,
                'time': self.CurrModelingTime,
                'x': rocket.coordinates[0],
                'y': rocket.coordinates[1],
                'z': rocket.coordinates[2],
            }

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
            z=launcher_data['start_coordinates']['z'],
            launcher_id=launcher_data['id']
        )

    def __checkTargetsLifeStatus(self):
        IsTargetsLive = True
        targetsStatus = []
        for target in self.targets.values():
            targetsStatus.append(target.Islive)
        if not any(targetsStatus):
            IsTargetsLive = False
        return IsTargetsLive

