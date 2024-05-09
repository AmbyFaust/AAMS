import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy.interpolate import interp1d


class Object:
    Id = 1


class LaunchSystem(Object):
    ObjectName = 'LaunchSystem'
    Id = 1

    def __init__(self, x, y, z, launcher_id=None):
        if launcher_id is None:
            self.Id = LaunchSystem.Id
            LaunchSystem.Id += 1
        else:
            self.Id = launcher_id
        self.coordinates = (x, y, z)
        self.max_range = 35000
        self.max_missiles = 6
        self.current_missiles_launched = 0
        self.remaining_missiles = self.max_missiles

    def launch_missile(self):
        if self.current_missiles_launched < self.max_missiles and self.remaining_missiles > 0:
            missile_id = str(self.Id) + "_missile_" + str(self.current_missiles_launched + 1)
            self.current_missiles_launched += 1
            self.remaining_missiles -= 1
            missile = Missile(self.coordinates)
            missile.set_target_coords((15000, 15000, 15000))  # Установка координат цели по умолчанию
            return missile
        else:
            print("Unable to launch missile. No available missiles left.")


class Missile(Object):
    def __init__(self, launch_coordinates):
        self.id = Object.Id
        Object.Id += 1
        self.speed = 1000
        self.coordinates = launch_coordinates
        self.target_coordinates = None
        self.trajectory = []  # Поле для хранения траектории полета

    def give_coords(self):
        return self.coordinates

    def set_target_coords(self, target_coords):
        self.target_coordinates = target_coords
        self.calculate_trajectory()  # Вычисляем траекторию при установке целевых координат

    def calculate_trajectory(self, step_size=1000):
        if self.target_coordinates is None:
            print("Cannot calculate trajectory. Target coordinates are not set.")
            return

        # Начальные координаты ракеты
        x1, y1, z1 = self.coordinates
        # Координаты цели
        x2, y2, z2 = self.target_coordinates

        # Вычисление длины линии между начальными и конечными точками
        distance = ((x2 - x1) ** 2 + (y2 - y1) ** 2 + (z2 - z1) ** 2) ** 0.5

        # Вычисление количества отрезков (точек), которые нужно разместить на траектории
        num_points = int(distance / step_size)

        # Массив для хранения координат точек траектории полета
        trajectory = []

        # Находим координаты точек на прямой для различных значений t
        for i in range(num_points + 1):
            t = i / num_points
            x = x1 + (x2 - x1) * t
            y = y1 + (y2 - y1) * t
            z = z1 + (z2 - z1) * t
            trajectory.append((x, y, z))

        self.trajectory = trajectory  # Сохраняем траекторию в поле объекта

    def detonate(self):
        if self.target_coordinates is not None:
            print(f"Missile {self.id} detonated at target coordinates {self.target_coordinates}.")
        else:
            print(f"Missile {self.id} cannot detonate without target coordinates.")

    def self_destruct(self):
        print(f"Missile {self.id} self-destructed.")

    def plot_trajectory(self):
        if not self.trajectory:
            print("Cannot plot trajectory. Trajectory is not calculated.")
            return

        # Разделение списка координат на отдельные списки x, y и z
        x_coords, y_coords, z_coords = zip(*self.trajectory)

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
    missile = launch_system.launch_missile()
    missile.plot_trajectory()
