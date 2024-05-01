from ObjectModels.CommandPostObj import CommandPostObj
from project.modeling.ObjectModels.RadarObj import RadarObj
from project.modeling.ObjectModels.RocketLauncherObj import RocketLauncherObj
from project.modeling.ObjectModels.SimpleTestPlane import SimpleTestPlane
import json

# Диспетчер моделирования
class SimulationManager:
    def __init__(self, StandartScenario = True, ConfigPath = 'ModelingConfigFile'):
        self.StandartScenario = StandartScenario
        self.ConfigPath = ConfigPath

# Функция считывает необходимую информацию для моделирования из файла
    def get_config_data(self):
        with open(self.ConfigPath) as json_file:
            ConfigInformation = json.load(json_file)

            #Функц
    def StandartScenarioConfig(self):
        pass

# Создание начальных объектов для моделирования
    def MakeScenarioObjects(self):
        if self.StandartScenario:
            ConfigInformation = self.StandartScenarioConfig()
        else:
            ConfigInformation = self.get_config_data()
        for ObjectInformation in ConfigInformation:
            MakeNewObject(ObjectInformation)




    def modeling(self):
        pass

    def modeling_step(self):
        pass


if __name__ == "__main__":
    SimulationManagerObj = SimulationManager("SimulationConfig")
    SimulationManagerObj.make_config_objects()