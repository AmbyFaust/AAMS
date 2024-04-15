from collections import namedtuple
import math
import numpy as np
import random

def get_x_y_z_from_r_u_v(a):
    r = a[0]
    u = a[1]
    v = a[2]
    x = r * math.cos(v) * math.cos(u)
    y = r * math.cos(v) * math.sin(u)
    z = r * math.sin(v)
    return [x, y, z]


def get_r_u_v_from_x_y_z(a):
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


class brunch(Object):
    marks = np.array([])
    next_gate = []
    initiated = True

def secondary_processing (x,y,z,r,u,v,stdU,stdV,stdR):
    trafectories = RadarObj.Trajectories # get all trajes
    if not trafectories:
        intitiate_traj(x,y,z,r,u,v)
    else:
        for one_traj in range (1,len(trafectories)+1):
            current_traj = trafectories[one_traj-1]
            if (current_traj.initiated == True):
                gates = current_traj.next_gate
                if (x > gates[0] and x < gates[1] and y > gates[2] and y < gates[3] and z > gates[4] and z < gates[5]):
                    curr_traj_marks = current_traj.marks
                    curr_coord = np.array([[r],[u],[v]])
                    current_traj.marks = np.concatenate((curr_traj_marks, curr_coord), axis=1)
                    current_traj.next_gate = get_tracking_gate(current_traj.marks,stdU,stdV,stdR)
                    current_traj.initiated = False
            else:
                gates = current_traj.next_gate
                if (r > gates[0] and r < gates[1] and u > gates[2] and u < gates[3] and v > gates[4] and v < gates[5]):
                    curr_traj_marks = current_traj.marks
                    curr_coord = np.array([[r],[u],[v]])
                    current_traj.marks = np.concatenate((curr_traj_marks, curr_coord), axis=1)
                    current_traj.next_gate = get_tracking_gate(current_traj.marks,stdU,stdV,stdR)
def intitiate_traj(x,y,z,r,u,v):
    creating_brunch = brunch;
    creating_brunch.marks = np.array([[r],[u],[v]])
    creating_brunch.next_gate = get_initation_gate(x,y,z)
    creating_brunch.initiated = True
    RadarObj.Trajectories.append(creating_brunch)

def get_initation_gate(x,y,z):
    initation_radius = t_btw_scanning * 500;
    return [x-initation_radius, x+initation_radius, y-initation_radius, y+initation_radius,z-initation_radius, z+initation_radius]

def get_tracking_gate(marks,stdU,stdV,stdR):
    prev_mark = marks[0:3, -2]
    last_mark = marks[0:3, -1]
    last_mark = get_x_y_z_from_r_u_v(last_mark)
    prev_mark = get_x_y_z_from_r_u_v(prev_mark)
    V_x = last_mark[0] - prev_mark[0]
    V_y = last_mark[1] - prev_mark[1]
    V_z = last_mark[2] - prev_mark[2]
    extr_x = last_mark[0] + V_x
    extr_y = last_mark[1] + V_y
    extr_z = last_mark[2] + V_z
    [r_extr,u_extr,v_extr] = get_r_u_v_from_x_y_z([extr_x,extr_y,extr_z])
    r1 = r_extr-3*stdR
    r2 = r_extr+3*stdR
    u1 = u_extr -3*stdU
    u2 = u_extr +3*stdU
    v1 = v_extr - 3*stdV
    v2 = v_extr + 3*stdV
    return [r1, r2, u1, u2, v1, v2]