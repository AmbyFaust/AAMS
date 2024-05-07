import json

from .ObjectModels.DataStructures import radar_params

from .ObjectModels.RadarObj import RadarObj
from .ObjectModels.TargetObj import Target

from .ObjectModels.CommandPostObj import CommandPostObj
from .ObjectModels.RocketLauncherObj import RocketLauncherObj
from .ObjectModels.SimpleTestPlane import SimpleTestPlane


class SimulationManager:
    def __init__(self):
        self.radars = []
        self.targets = []

    def load_from_file(self, path):
        with open(path, 'r') as file:
            d = json.load(file)
            self.radars = d['objects']['radars']
            self.targets = d['objects']['targets']

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
                start_coords=radar_data['start_coordinates'],
                SNRDetection=radar_data['snr_detection']
            ), radar_id=radar_data['id'])
        )

    def __load_target_object(self, target_data):
        self.targets.append(

        )


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