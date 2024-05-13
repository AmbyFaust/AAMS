import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy.interpolate import interp1d
from project.modeling.ObjectModels.Object import Object
from collections import namedtuple
RectCS = namedtuple('RectCS', 'X Y Z')


class LaunchSystem(Object):
    ObjectName = 'LaunchSystem'
    Id = 1

    def __init__(self, x, y, z, launcher_id=None):
        if launcher_id is None:
            self.Id = LaunchSystem.Id
            LaunchSystem.Id += 1
        else:
            self.Id = launcher_id
        self.radarId = []
        self.coordinates = RectCS(X=x, Y=y, Z=z)
        self.max_range = 35000
        self.max_missiles = 6
        self.current_missiles_launched = 0
        self.remaining_missiles = self.max_missiles

    def launch_missile(self, radarId, targetId, time):
        if self.current_missiles_launched < self.max_missiles and self.remaining_missiles > 0:
            missile_id = str(self.Id) + "_missile_" + str(self.current_missiles_launched + 1)
            self.current_missiles_launched += 1
            self.remaining_missiles -= 1
            missile = Missile(radarId,targetId, self.coordinates,time)
            missile.radarId = radarId
            missile.targetId = targetId
            missile.changeDirectionofFlight((15000, 15000, 15000))  # Установка координат цели по умолчанию
            return missile
        else:
            print("Unable to launch missile. No available missiles left.")


class Missile(Object):
    ObjectName = 'Rocket'
    Id = 1
    def __init__(self,radarId,targetId, launch_coordinates, time):
        self.id = Missile.Id
        self.radarId = radarId
        self.targetId = targetId
        Missile.Id += 1
        self.speed = 1000
        self.coordinates = launch_coordinates
        self.time = time
        self.target_coordinates = None
        self.trajectory = []  # Поле для хранения траектории полета
        self.rocket_trajectory = [launch_coordinates]
        self.DetonationRange = 100
        self.DamageRange = 200

    def give_coords(self):
        return self.coordinates

    def changeDirectionofFlight(self, target_coords):
        self.target_coordinates = target_coords
        self.calculate_trajectory()  # Вычисляем траекторию при установке целевых координат


    def checkDetonationConditions(self, targets):
        bum = False
        for target in targets:
            direction_vector = np.array(target.CurrCoords) - np.array(self.coordinates)

            # Вычисляем длину вектора направления
            dist = np.linalg.norm(direction_vector)

            if self.DetonationRange >= dist:
                bum = True
                self.detonate(target)
        if bum == True:
            for target in targets:
                direction_vector = np.array(target.CurrCoords) - np.array(self.coordinates)

                # Вычисляем длину вектора направления
                dist = np.linalg.norm(direction_vector)

                if self.DamageRange >= dist:
                    self.detonate(target)


    def move(self, time):
        CalculatedCoords = self.get_coordinates_at_time(time)
        self.time = time
        self.coordinates = CalculatedCoords
        #print('self.coordinates after move = ', self.coordinates)
        self.rocket_trajectory.append(self.coordinates)
        pass

    def distance_to_target(self):
        direction_vector = np.array(self.target_coordinates) - np.array(self.coordinates)
        # Вычисляем длину вектора направления
        distance = np.linalg.norm(direction_vector)
        return distance

    def calculate_trajectory(self, step_size=10):
        if self.target_coordinates is None:
            #print("Cannot calculate trajectory. Target coordinates are not set.")
            return

        #print('self.coordinates = ', self.coordinates)
        #print('self.target_coordinates = ', self.target_coordinates)

        x1, y1, z1 = self.coordinates
        # Координаты цели
        x2, y2, z2 = self.target_coordinates
        # Вычисление длины линии между начальными и конечными точками
        distance = self.distance_to_target()

        # Вычисление количества отрезков (точек), которые нужно разместить на траектории
        num_points = int(distance / step_size) + 1

        # Массив для хранения координат точек траектории полета

        # Находим координаты точек на прямой для различных значений t
        for i in range(num_points + 1):
            t = i / num_points
            x = x1 + (x2 - x1) * t
            y = y1 + (y2 - y1) * t
            z = z1 + (z2 - z1) * t
            self.trajectory.append(RectCS(X=x, Y=y, Z=z))

      # Сохраняем траекторию в поле объекта

    def get_coordinates_at_time(self, time):


        if self.target_coordinates is None:
            print("Cannot get coordinates. Target coordinates are not set.")
            return None

        if not self.coordinates:
            print("Cannot get coordinates. Initial coordinates are not set.")
            return None

        # Вычисляем вектор направления к цели
        direction_vector = np.array([self.target_coordinates[0] - self.coordinates[0],
                                     self.target_coordinates[1] - self.coordinates[1],
                                     self.target_coordinates[2] - self.coordinates[2]])

        # Вычисляем длину вектора направления
        direction_length = np.linalg.norm(direction_vector)

        # Нормализуем вектор направления
        direction_unit_vector = direction_vector / direction_length

        # Вычисляем дистанцию, которую прошла ракета за заданное время
        distance_traveled = self.speed * (time - self.time)

        # Если дистанция превышает расстояние до цели, то ракета достигла цели
        if distance_traveled > direction_length:
            print('Error')
            return None
        '''
        print('self.coordinates.X = ', self.coordinates.X)
        print('direction_unit_vector[0] = ', direction_unit_vector[0])
        print('distance_traveled = ', distance_traveled)
        '''

        # Вычисляем новые координаты ракеты
        new_x = self.coordinates.X + direction_unit_vector[0] * distance_traveled
        new_y = self.coordinates.Y + direction_unit_vector[1] * distance_traveled
        new_z = self.coordinates.Z + direction_unit_vector[2] * distance_traveled

        #print('new_x = ', new_x)

        new_coordinates = RectCS(X=new_x, Y=new_y, Z=new_z)

        return new_coordinates

    def detonate(self, target):
        if self.target_coordinates is not None:
            print(f"Missile {self.id} detonated at target coordinates {self.target_coordinates}.")
            self.Islive = False
            target.Islive = False
        else:
            print(f"Missile {self.id} cannot detonate without target coordinates.")

    def self_destruct(self):
        self.Islive = False
        print(f"Missile {self.id} self-destructed.")



    def plot_trajectory(self):
        if not self.trajectory:
            print("Cannot plot trajectory. Trajectory is not calculated.")
            return

        # Разделение списка координат на отдельные списки x, y и z
        x_coords, y_coords, z_coords = zip(*self.rocket_trajectory)

        # Создание 3D-графика траектории
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.plot(x_coords, y_coords, z_coords, label=f'Missile trajectory')

        # Пометка начальной точки
        ax.scatter(x_coords[0], y_coords[0], z_coords[0], c='r', marker='o', label='Starting Point')

        # Если установлена новая цель в середине полета, пометим ее красным цветом
        if self.target_coordinates:
            target_x, target_y, target_z = self.target_coordinates
            ax.scatter(target_x, target_y, target_z, c='r', marker='x', label='New Target')

        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        ax.legend()
        plt.show()


if __name__ == '__main__':
    launch_system = LaunchSystem(0, 0, 0)
    missile = launch_system.launch_missile(0, 1, 0)
    missile.move(25)
    missile.changeDirectionofFlight((30000,30000,0))
    missile.move(32)
    missile.changeDirectionofFlight((45000, 45000, 45000))
    missile.move(60)
    missile.changeDirectionofFlight((5000, 5000, 45000))
    missile.move(102.6)
    print(missile.distance_to_target())
    missile.plot_trajectory()




