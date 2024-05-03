import typing

from .base_entity import BaseEntity
from .coordinates_entity import CoordinatesEntity
from ... import TypeTargetEnum
from ...settings import SPEED, TARGET_TYPE, SCS


class TargetEntity(BaseEntity):
    def __init__(self, id: int = None, coordinates: typing.List[CoordinatesEntity] = None,
                 speed: int = SPEED, target_type: TypeTargetEnum = TARGET_TYPE,
                 scs: int = SCS):
        super(TargetEntity, self).__init__(id=id)
        self.coordinates = coordinates
        self.speed = speed
        self.target_type = target_type
        self.scs = scs
