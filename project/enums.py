from enum import Enum


class ObjectEnum(Enum):
    RLS = (0, 'РЛС')
    TARGET = (1, 'Цель')

    def __init__(self, num, desc):
        self.num = num
        self.desc = desc