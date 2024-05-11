import typing

from .base_entity import BaseEntity
from .coordinates_entity import CoordinatesEntity
from ... import TypeTargetEnum
from ...settings import SPEED, TARGET_TYPE, EPR


class TargetEntity(BaseEntity):
    def __init__(self, id: int = None, coordinates: typing.List[CoordinatesEntity] = None,
                 speed: int = SPEED, target_type: TypeTargetEnum = TARGET_TYPE,
                 epr: int = EPR):
        super(TargetEntity, self).__init__(id=id)
        self.coordinates = coordinates
        self.speed = speed
        self.target_type = target_type
        self.epr = epr

    def to_dict(self):
        return {
            'id': self.id,
            'coordinates': [c.to_dict() for c in self.coordinates],
            'speed': self.speed,
            'type': self.target_type.desc,
            'epr': self.epr
        }

    def from_dict(self, data):
        self.id = data['id']
        self.coordinates = [CoordinatesEntity().from_dict(data['coordinates'][i])
                            for i in range(len(data['coordinates']))]
        self.speed = data['speed']
        self.target_type = TypeTargetEnum.get_target_type_from_desc(data['type'])
        self.epr = data['epr']
        return self
