from project.modeling.ObjectModels.Object import Object, MovebleObject
from project.modeling.ObjectModels.DataStructures import  RectCS, target_params
import numpy as np
class SimpleTestPlane(MovebleObject):
    ObjectName = 'Plane'
    def __init__(self):
        self.Id = Object.Id
        Object.Id +=1
        self.StartCoords = RectCS(X=15000, Y=0, Z=0)
        self.Velocity = RectCS(X=-100, Y=0, Z=0)
        self.ObjCoords = self.StartCoords

    def CalcCoord(self, time):
        X = self.StartCoords.X + self.Velocity.X * time
        Y = self.StartCoords.Y + self.Velocity.Y * time
        Z = self.StartCoords.Z + self.Velocity.Z * time
        return RectCS(X=X, Y=Y, Z=Z)

    def ReturnPlaneInformation(self,time):
        CalculatedCoords =self.CalcCoords(time)
        return target_params(RCS=self.RCS, coordinates=CalculatedCoords)

if __name__ == "__main__":
    testPlane1 = SimpleTestPlane()
    testPlane2 = SimpleTestPlane()
    times = np.linspace(0,1,100)
    for time in times:
        CalculateCoords = testPlane1.CalcCoord(time)
        testPlane1.move(CalculateCoords)
        print(testPlane1)
        print(testPlane2)
