import collections
import math
import numpy as np


# Перевод из ГПСК В МПСК
def GRCStoLRCS(GRCSCoords, AnchorPoint):
    pass


# Перевод из МПСК в ГПСК
def LRCStoGRCS(X, Y, Z):
    pass


# Перевод из МПСК в обобщённую СК
def GRCStoUV(a):

    pass
def get_x_y_z_from_r_u_v(a):

    return [x, y, z]

def UVtoGRCS(a):
    r = a[0]
    u = a[1]
    v = a[2]
    x = r * math.cos(v) * math.cos(u)
    y = r * math.cos(v) * math.sin(u)
    z = r * math.sin(v)
    return [x,y,z]


def GRCStoUV(a):
    x = a[0]
    y = a[1]
    z = a[2]
    r = pow((pow(x, 2) + pow(y, 2) + pow(z, 2)), 0.5)

    if (x >= 0):
        u = math.atan(y / x)
    if (x < 0 and y >= 0):
        u = np.pi / 2 - math.atan(y / x)
    if (x < 0 and y < 0):
        u = -np.pi / 2 + math.atan(y / x)
    v = math.asin(z / r)
    return [r, u, v]
