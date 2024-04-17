from enum import Enum


class ObjectEnum(Enum):
    SAR = (0, 'РЛС')
    TARGET = (1, 'Цель')

    def __init__(self, num: int, desc: int):
        self.num = num
        self.desc = desc
