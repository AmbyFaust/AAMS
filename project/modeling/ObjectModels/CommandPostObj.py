from project.modeling.ObjectModels.Object import Object
import math


class CommandPostObj(Object):
    detect_id_object = []
    def tritial_processing(self, all_radars,current_traj):
        if current_traj.target_id in self.detect_id_object:
            pass
        else:
            self.detect_id_object.append(current_traj.target_id)
            convinient_radar = self.find_convinient_radar(all_radars,current_traj)
            launched_rocket = Missile()
            launched_rocket.radarId = convinient_radar.Id
            launched_rocket.targetId = current_traj.target_id
            print('The launcher of the radar with id ', convinient_radar.Id, ' launched a rocket to liquidate ',
                  current_traj.target_id)
        return launched_rocket




    def find_convinient_radar(self, all_radars,current_traj):
        [x, y, z] = current_traj.stack_of_coords[:, -1]
        all_ranges = []
        for radar in all_radars:
            rad_coords = radar.StartCoords
            x0 = rad_coords.X
            y0 = rad_coords.Y
            z0 = rad_coords.Z
            all_ranges.append(math.sqrt((x - x0) ** 2 + (y - y0) ** 2 + (z - z0) ** 2))
        min_value = min(all_ranges)
        min_index = all_ranges.index(min_value)
        convinient_radar = all_radars[min_index]
        return convinient_radar




if __name__ == "__main__":
    enme = CommandPostObj()
    print('Классы компилируются')
