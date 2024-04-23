from DataStructures import RectCS


class Object:
    Id = 1
    ObjectName = 'SimpleObject'
    Islive = True

    def __init__(self, startcoods=RectCS(X=0, Y=0, Z=0)):
        self.Id = Object.Id
        Object.Id += 1
        self.StartCoords = startcoods
        self.ObjCoords = startcoods

    def __str__(self):
        return self.ObjectName + str(self.Id) + ' with coords ' + str(self.ObjCoords)

    def destroyed(self):
        self.Islive = False
        tmpString = self.ObjectName + str(self.Id)
        print(tmpString, 'has been destroyed')


class MovebleObject(Object):
    ObjectName = 'MovebleSimpleObject'

    def move(self, NewCoords):
        self.ObjCoords = NewCoords
        tmpString = self.ObjectName + str(self.Id)
        print(tmpString, 'move to', NewCoords)


if __name__ == "__main__":
    print('Классы компилируются')
    simpleObj = Object()
    movebleobj1 = MovebleObject()
    print(simpleObj.Id)
    # print("ObjectID =", Object.Id)
    # print("SimpleObjectID =", simpleObj.Id)
    # print(objcoords)
    newPoint = RectCS(X=3, Y=4, Z=5)
    print(simpleObj)
    simpleObj.destroyed()
    print(movebleobj1)
    movebleobj1.move(newPoint)
    print(movebleobj1)
