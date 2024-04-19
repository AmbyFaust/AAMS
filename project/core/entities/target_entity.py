from .base_entity import BaseEntity
from .coordinates_entity import CoordinatesEntity


class TargetEntity(BaseEntity):
    def __init__(self, id: int = None, coordinates: CoordinatesEntity = None):
        super(TargetEntity, self).__init__(id=id)
        self.coordinates = coordinates
