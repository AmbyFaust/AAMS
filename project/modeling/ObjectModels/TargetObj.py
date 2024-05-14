import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
from collections import namedtuple
from project.modeling.ObjectModels.DataStructures import  RectCS, target_params
from project.modeling.ObjectModels.Object import Object


class Target(Object):
    ObjectName = 'Target'
    Id = 1

    def __init__(self, type, ObjectName, epr, velocity, control_points, target_id=None):
        if target_id is None:
            self.Id = Target.Id
            Target.Id += 1
        else:
            self.Id = target_id
        self.type = type
        self.ObjectName = ObjectName
        self.epr = epr
        self.velocity = velocity
        self.control_points = [RectCS(X=p['x'], Y=p['y'], Z=p['z']) for p in control_points]
        self.CurrCoords = self.control_points[0]
        self.coordinates_dict = self._generate_coordinates_dict()

    def _generate_coordinates_dict(self):
        x_coords = [point[0] for point in self.control_points]
        y_coords = [point[1] for point in self.control_points]
        z_coords = [point[2] for point in self.control_points]

        spline_x = interp1d(np.arange(len(self.control_points)), x_coords, kind='cubic')
        spline_y = interp1d(np.arange(len(self.control_points)), y_coords, kind='cubic')
        spline_z = interp1d(np.arange(len(self.control_points)), z_coords, kind='cubic')


        num_points = 100  # Изменим коэффициент на 10
        t = np.linspace(0, len(self.control_points) - 1, num_points)
        x_interp = spline_x(t)
        y_interp = spline_y(t)
        z_interp = spline_z(t)


        coordinates_dict = {}
        # for i in range(len(self.control_points)):
        #    coordinates_dict[i] = (self.control_points[i][0], self.control_points[i][1])
        # for i in range(num_points):
        #   coordinates_dict[i] = (x_interp[i], y_interp[i])
        # return coordinates_dict

        t = 0
        coordinates_dict[0] = [x_interp[0], y_interp[0], z_interp[0], t]
        for i in range(1, num_points):
            distance = ((x_interp[i] - x_interp[i - 1]) ** 2 + (y_interp[i] - y_interp[i - 1]) ** 2 + (z_interp[i] - z_interp[i - 1]) ** 2) ** 0.5
            t += distance / self.velocity
            coordinates_dict[i] = [x_interp[i], y_interp[i], z_interp[i], t]
        return coordinates_dict

    def move(self, time):
        CalculatedCoords = self.calculate_position_at_time(time)
        self.CurrCoords = CalculatedCoords
        pass

    def calculate_position_at_time(self, time):
        # Находим ближайшие времена до и после заданного времени
        times = np.array(list(self.coordinates_dict.values()))[:, 3]
        nearest_times = times[times <= time]
        prev_time = nearest_times[-1] if nearest_times.size > 0 else times[0]
        next_time = times[times > time][0] if times.size > nearest_times.size else times[-1]

        # Получаем координаты точек, соответствующих ближайшим временам
        prev_coords = self.coordinates_dict[
            next((key for key, value in self.coordinates_dict.items() if value[-1] == prev_time), None)]
        next_coords = self.coordinates_dict[
            next((key for key, value in self.coordinates_dict.items() if value[-1] == next_time), None)]

        # Интерполируем координаты между ближайшими точками по времени
        interp_coords = np.array(prev_coords[:3]) + ((time - prev_coords[3]) / (next_coords[3] - prev_coords[3])) * (
                np.array(next_coords[:3]) - np.array(prev_coords[:3]))

        return RectCS(X=interp_coords[0], Y=interp_coords[1], Z=interp_coords[2])

    def ReturnPlaneInformation(self,time):
        CalculatedCoords =self.calculate_position_at_time(time)
        return target_params(RCS=self.epr, coordinates=CalculatedCoords, TargetId=self.Id)

    def plot_trajectory(self):

        # control_x, control_y = zip(*[(point[0], point[1]) for point in self.control_points])
        # plt.scatter(control_x, control_y, c='red', marker='o', label='Контрольные точки')
        interp_x, interp_y, interp_z = zip(*[(point[0], point[1], point[2]) for point in list(self.coordinates_dict.values())])
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        ax.plot(interp_x, interp_y, interp_z, label=f'Target trajectory')
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        ax.legend()
        plt.show()

if __name__ == '__main__':
    control_points = [
        (0, 0, 10000),
        (10000, 10000, 10000),
        (20000, 5000, 10000),
        (30000, 10000, 10000)
    ]
    target = Target("jet", "F-15", 1, 400, control_points)
    target.plot_trajectory()
    coordinates_dict = target.coordinates_dict
    coords = target.calculate_position_at_time(9)
    #inf = target.ReturnPlaneInformation(9)
    #print(inf)
    print(coords)
    print(coordinates_dict)
