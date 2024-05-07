from .base_entity import BaseEntity
from .coordinates_entity import CoordinatesEntity
from ...settings import (EIRP, SEFF, BW_U, BW_V, SCANNING_V, T_N, PRF, N_PULSES_PROC,
                         OPERATING_FREQ, START_TIME, SNR_DETECTION)


class RadarEntity(BaseEntity):
    def __init__(self, id: int = None, coordinates: CoordinatesEntity = None,
                 eirp: int = EIRP,
                 seff: int = SEFF,
                 bw_u: int = BW_U,
                 bw_v: int = BW_V,
                 scanning_v: int = SCANNING_V,
                 t_n: int = T_N,
                 prf: int = PRF,
                 n_pulses_proc: int = N_PULSES_PROC,
                 operating_freq: int = OPERATING_FREQ,
                 start_time: int = START_TIME,
                 snr_detection: int = SNR_DETECTION
                 ):
        super(RadarEntity, self).__init__(id=id)
        self.start_coordinates = coordinates  # RectCS
        self.eirp = eirp    # Эффективная изотропная излучаемая мощность > 0
        self.seff = seff    # Эффективная площадь антенны > 0
        self.bw_u = bw_u    # ширина луча по азимуту в градусах 0 < BW_U < 45
        self.bw_v = bw_v    # ширина луча по углу места в градусах 0 < BW_V < 45
        self.scanning_v = scanning_v    # пределы сканирования по углу места (list[от ;до])
        self.t_n = t_n  # Шумовая температура в Кельвинаx > комнатной температуры
        self.prf = prf  # Частота повторения импульсов PRF > 2/SignalTime
        self.n_pulses_proc = n_pulses_proc  # количество импульсов в пачке (в одном положении луча)
        self.operating_freq = operating_freq # Рабочая частота(обычно МГц или ГГц)
        self.start_time = start_time
        self.snr_detection = snr_detection  # ОСШ для обнаружения > 0

    def to_dict(self):
        return {
            'id': self.id,
            'start_coordinates': self.start_coordinates.to_dict(),
            'eirp': self.eirp,
            'seff': self.seff,
            'bw_u': self.bw_u,
            'bw_v': self.bw_v,
            'scanning_v': self.scanning_v,
            't_n': self.t_n,
            'prf': self.prf,
            'n_pulses_proc': self.n_pulses_proc,
            'operating_freq': self.operating_freq,
            'start_time': self.start_time,
            'snr_detection': self.snr_detection
        }

    def from_dict(self, data):
        self.id = data['id']
        self.start_coordinates = CoordinatesEntity().from_dict(data['coordinates'])
        self.eirp = data['eirp']
        self.seff = data['seff']
        self.bw_u = data['bw_u']
        self.bw_v = data['bw_v']
        self.scanning_v = data['scanning_v']
        self.t_n = data['t_n']
        self.prf = data['prf']
        self.n_pulses_proc = data['n_pulses_proc']
        self.operating_freq = data['operating_freq']
        self.start_time = data['start_time']
        self.snr_detection = data['snr_detection']
        return self
