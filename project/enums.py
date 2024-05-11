from enum import Enum


class ObjectEnum(Enum):
    RADAR = (0, 'РЛС')
    TARGET = (1, 'Цель')

    def __init__(self, num: int, desc: int):
        self.num = num
        self.desc = desc


class TypeTargetEnum(Enum):
    first = (0, 'Первый')
    second = (1, 'Второй')

    def __init__(self, num: int, desc: int):
        self.num = num
        self.desc = desc

    @classmethod
    def get_target_type_from_desc(cls, desc: str):
        for target_type in cls:
            if target_type.desc == desc:
                return target_type

        return cls.first
