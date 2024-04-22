from enum import Enum


class ObjectEnum(Enum):
    SAR = (0, 'РЛС')
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


