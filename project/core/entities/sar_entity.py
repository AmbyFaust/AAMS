from .base_entity import BaseEntity
from .coordinates_entity import CoordinatesEntity


class SarEntity(BaseEntity):
    def __init__(self, id: int = None, coordinates: CoordinatesEntity = None):
        super(SarEntity, self).__init__(id=id)
        self.coordinates = coordinates

