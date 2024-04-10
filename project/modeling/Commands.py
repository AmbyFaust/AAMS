from abc import ABC, abstractmethod


class Command(ABC):

    @abstractmethod
    def execute(self):
        ...


class MakeMeasurementCommand(Command):
    def execute(self):
        print('ok')


if __name__ == "__main__":
    ab = MakeMeasurementCommand()
    ab.execute()
