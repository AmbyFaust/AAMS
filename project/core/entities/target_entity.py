from .base_entity import BaseEntity
from .coordinates_entity import CoordinatesEntity
from ... import TypeTargetEnum


class TargetEntity(BaseEntity):
    def __init__(self, id: int = None, coordinates: list[CoordinatesEntity] = None,
                 speed: int = 100, type: TypeTargetEnum = TypeTargetEnum.first,
                 scs: int = 100, height: int = 100):
        super(TargetEntity, self).__init__(id=id)
        self.coordinates = coordinates
        self.speed = speed
        self.type = type
        self.scs = scs
        self.height = height
