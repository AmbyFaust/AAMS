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



