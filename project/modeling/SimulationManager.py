import json

from .ObjectModels.DataStructures import radar_params

from .ObjectModels.RadarObj import RadarObj
from .ObjectModels.TargetObj import Target
from .ObjectModels.Launcher_and_missile import LaunchSystem


class SimulationManager:
    def __init__(self, path):
        self.path = path
        self.radars = []
        self.targets = []
        self.launchers = []

    def load_objects(self):
        with open(self.path, 'r', encoding='utf-8') as file:
            d = json.load(file)

            for radar_data in d['objects']['radars']:
                self.__load_radar_object(radar_data)
                self.__load_launcher_object(radar_data)

            for target_data in d['objects']['targets']:
                self.__load_target_object(target_data)

    def modeling(self):
        pass

    def modeling_step(self):
        pass

    def __load_radar_object(self, radar_data):
        self.radars.append(
            RadarObj(radar_params(
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
                start_coords=tuple(radar_data['start_coordinates'].values()),
                SNRDetection=radar_data['snr_detection']
            ), radar_id=radar_data['id'])
        )

    def __load_target_object(self, target_data):
        self.targets.append(
            Target(
                type=target_data['type'],
                ObjectName='{}_{}'.format(target_data['type'], target_data['id']),
                epr=target_data['epr'],
                velocity=target_data['speed'],
                control_points=[(p['x'], p['y'], p['z']) for p in target_data['coordinates']],
                target_id=target_data['id']
            )
        )

    def __load_launcher_object(self, launcher_data):
        self.launchers.append(
            LaunchSystem(
                x=launcher_data['start_coordinates']['x'],
                y=launcher_data['start_coordinates']['y'],
                z=launcher_data['start_coordinates']['x'],
                launcher_id=launcher_data['id']
            )
        )

    def __append_data(self, data):
        new_row_id = 0
        with open(self.path, 'r+') as file:
            d = json.load(file)

            if len(d['data']) > 0:
                new_row_id = max(d['data'].keys()) + 1

            for row in data:
                d['data'][new_row_id] = {
                    'radar_id': row['radar_id'],
                    'target_id': row['target_id'],
                    'time': row['time'],
                    'x': row['x'],
                    'y': row['y'],
                    'z': row['z']
                }
                new_row_id += 1

            json.dump(d, file)


# Диспетчер моделирования
# class SimulationManager:
#     def __init__(self, StandartScenario = True, ConfigPath = 'ModelingConfigFile'):
#         self.StandartScenario = StandartScenario
#         self.ConfigPath = ConfigPath
#
#     # Функция считывает необходимую информацию для моделирования из файла
#     def get_config_data(self):
#         with open(self.ConfigPath) as json_file:
#             ConfigInformation = json.load(json_file)
#
#             #Функц
#     def StandartScenarioConfig(self):
#         pass
#
#     # Создание начальных объектов для моделирования
#     def MakeScenarioObjects(self):
#         if self.StandartScenario:
#             ConfigInformation = self.StandartScenarioConfig()
#         else:
#             ConfigInformation = self.get_config_data()
#         for ObjectInformation in ConfigInformation:
#             MakeNewObject(ObjectInformation)
#
#
#     def modeling(self):
#         pass
#
#     def modeling_step(self):
#         pass


if __name__ == "__main__":
    SimulationManagerObj = SimulationManager("SimulationConfig")
    SimulationManagerObj.make_config_objects()