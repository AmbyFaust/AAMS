from project.modeling.ObjectModels.Object import Object, MovebleObject
from project.modeling.ObjectModels.DataStructures import  RectCS, target_params
import numpy as np
class SimpleTestPlane(MovebleObject):
    ObjectName = 'Plane'
    Id = 1
    def __init__(self):
        self.Id = SimpleTestPlane.Id
        SimpleTestPlane.Id += 1
        self.StartCoords = RectCS(X=15000, Y=0, Z=1000)
        self.Velocity = RectCS(X=-100, Y=0, Z=0)
        self.ObjCoords = self.StartCoords
        self.RCS = 10

    def CalcCoord(self, time):
        X = self.StartCoords.X + self.Velocity.X * time
        Y = self.StartCoords.Y + self.Velocity.Y * time
        Z = self.StartCoords.Z + self.Velocity.Z * time
        return RectCS(X=X, Y=Y, Z=Z)

    def ReturnPlaneInformation(self,time):
        CalculatedCoords =self.CalcCoord(time)
        return target_params(RCS=self.RCS, coordinates=CalculatedCoords, TargetId=self.Id)

if __name__ == "__main__":
    testPlane1 = SimpleTestPlane()
    testPlane2 = SimpleTestPlane()
    times = np.linspace(0,1,100)
    for time in times:
        CalculateCoords = testPlane1.CalcCoord(time)
        testPlane1.move(time)

