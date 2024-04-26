from .base_entity import BaseEntity
from .coordinates_entity import CoordinatesEntity
from ... import settings


class SarEntity(BaseEntity):
    def __init__(self, id: int = None, coordinates: CoordinatesEntity = None, radius: int = settings.SAR_RADIUS):
        super(SarEntity, self).__init__(id=id)
        self.coordinates = coordinates
        self.radius = radius


