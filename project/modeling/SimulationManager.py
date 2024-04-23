from ObjectModels.CommandPostObj import CommandPostObj
import json
class SimulationManager:
    def __init__(self, StandartScenario = True, ConfigPath = 'ModelingConfigFile'):
        self.StandartScenario = StandartScenario
        self.ConfigPath = ConfigPath

    def get_config_data(self):
        with open(self.ConfigPath) as json_file:
            ConfigInformation = json.load(json_file)
    def StandartScenarioConfig(self):
        pass

    def MakeScenarioObjects(self):
        if self.StandartScenario:
            ConfigInformation = self.StandartScenarioConfig()
        else:
            ConfigInformation = self.get_config_data()
        for ObjectInformation in ConfigInformation:
            switch


    def modeling(self):
        pass

    def modeling_step(self):
        pass


if __name__ == "__main__":
    SimulationManagerObj = SimulationManager("SimulationConfig")
    SimulationManagerObj.make_config_objects()