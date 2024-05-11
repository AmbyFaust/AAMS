from project.modeling.ObjectModels.TargetObj import Target

control_points = [
    (0, 0, 0),
    (10000, 10000, 0),
    (20000, 5000, 0),
    (30000, 10000, 0)
]
target = Target("jet", "F-15", 1, 400, control_points)
target.plot_trajectory()
coordinates_dict = target.coordinates_dict
coords = target.calculate_position_at_time(9)
inf = target.ReturnPlaneInformation(9)
print(inf)
print(coords)
print(coordinates_dict)