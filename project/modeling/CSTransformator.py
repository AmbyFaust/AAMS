import collections
from project.modeling.ObjectModels.DataStructures import UVCS, RectCS
import math
import numpy as np


# Перевод из ГПСК В МПСК
def GRCStoLRCS(GRCSCoords, AnchorPoint):
    LRCSTargCoords = RectCS(X=GRCSCoords.X - AnchorPoint.X, Y=GRCSCoords.Y - AnchorPoint.Y,
                            Z=GRCSCoords.Z - AnchorPoint.Z)
    return(LRCSTargCoords)


# Перевод из МПСК в ГПСК
def LRCStoGRCS(LRCSTargCoords, AnchorPoint):
    GRCSTargCoords = RectCS(X=LRCSTargCoords.X+AnchorPoint.X, Y=LRCSTargCoords.Y+AnchorPoint.Y,
                            Z=LRCSTargCoords.Z+AnchorPoint.Z)
    return GRCSTargCoords


# Перевод из МПСК в обобщённую СК
def GRCStoUV(GRCSTargCoords,AnchorPoint):
    LRCSTargCoords = GRCStoLRCS(GRCSTargCoords,AnchorPoint)
    return LRCStoUV(LRCSTargCoords)

def UVtoGRCS(UVTargCoords,AnchorPoint):
    LRCSTargCoords = UVtoLRCS(UVTargCoords)
    return LRCStoGRCS(LRCSTargCoords,AnchorPoint)



def UVtoLRCS(UVTargCoords):#
    r = UVTargCoords.R
    u = UVTargCoords.U
    v = UVTargCoords.V
    x = r * math.cos(v) * math.cos(u)
    y = r * math.cos(v) * math.sin(u)
    z = r * math.sin(v)
    return RectCS(X=x, Y=y, Z=z)


def LRCStoUV(LRCSTargCoords):
    x = LRCSTargCoords.X
    y = LRCSTargCoords.Y
    z = LRCSTargCoords.Z
    r = pow((pow(x, 2) + pow(y, 2) + pow(z, 2)), 0.5)

    if x >= 0:
        u = math.atan(y / x)
    if (x < 0 and y >= 0):
        u = np.pi / 2 - math.atan(y / x)
    if (x < 0 and y < 0):
        u = -np.pi / 2 + math.atan(y / x)
    v = math.asin(z / r)

    return UVCS(R=r,U=math.degrees(u),V=math.degrees(v))
