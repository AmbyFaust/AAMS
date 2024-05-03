import typing

from .base_entity import BaseEntity
from .coordinates_entity import CoordinatesEntity
from ... import TypeTargetEnum
from ... import settings


class TargetEntity(BaseEntity):
    def __init__(self, id: int = None, coordinates: typing.List[CoordinatesEntity] = None,
                 speed: int = settings.SPEED, target_type: TypeTargetEnum = settings.TARGET_TYPE,
                 scs: int = settings.SCS):
        super(TargetEntity, self).__init__(id=id)
        self.coordinates = coordinates
        self.speed = speed
        self.target_type = target_type
        self.scs = scs
