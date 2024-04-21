from ObjectModels.CommandPostObj import CommandPostObj
import json
class SimulationManager:
    ConfigPath = "RadarConfiguration"
    def __init__(self, ConfigPath):
        self.ConfigPath

    def get_config_data(self):
        pass

    def make_config_objects(self):
        with open(self.ConfigPath) as json_file:
            ConfigInformation = json.load(json_file)

        self.Rockets = {}
        self.CommandPostObj = CommandPostObj()
        self.Radars = {}
        self.RocketLaunchers = {}
        self.Targets = {}


    def modeling(self):
        pass

    def modeling_step(self):
        pass


if __name__ == "__main__":
    SimulationManagerObj = SimulationManager("SimulationConfig")
    SimulationManagerObj.make_config_objects()