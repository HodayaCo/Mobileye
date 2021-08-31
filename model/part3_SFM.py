import numpy as np
import math


def calc_TFL_dist(prev_container, curr_container, focal, pp):
    norm_prev_pts, norm_curr_pts, R, foe, tZ = prepare_3D_data(prev_container, curr_container, focal, pp)
    if (abs(tZ) < 10e-6):
        print('tz = ', tZ)
    elif (norm_prev_pts.size == 0):
        print('no prev points')
    elif (norm_curr_pts.size == 0):
        print('no curr points')
    else:
        curr_container.corresponding_ind, curr_container.traffic_lights_3d_location, curr_container.valid = calc_3D_data(
            norm_prev_pts, norm_curr_pts, R, foe, tZ)
    return curr_container


def prepare_3D_data(prev_container, curr_container, focal, pp):
    #norm_prev_pts = normalize(np.array(list(prev_container.red_traffic_light) + list(prev_container.green_traffic_light)), focal, pp)
    #norm_curr_pts = normalize(np.array(list(curr_container.red_traffic_light) + list(curr_container.green_traffic_light)), focal, pp)
    norm_prev_pts = normalize(prev_container.traffic_light, focal, pp)
    norm_curr_pts = normalize(curr_container.traffic_light, focal, pp)
    R, foe, tZ = decompose(curr_container.EM)
    return norm_prev_pts, norm_curr_pts, R, foe, tZ


def calc_3D_data(norm_prev_pts, norm_curr_pts, R, foe, tZ):
    norm_rot_pts = rotate(norm_prev_pts, R)
    pts_3D = []
    corresponding_ind = []
    validVec = []
    for p_curr in norm_curr_pts:
        corresponding_p_ind, corresponding_p_rot = find_corresponding_points(p_curr, norm_rot_pts, foe)
        Z = calc_dist(p_curr, corresponding_p_rot, foe, tZ)
        valid = (Z > 0)
        if not valid:
            Z = 0
        validVec.append(valid)
        P = Z * np.array([p_curr[0], p_curr[1], 1])
        pts_3D.append((P[0], P[1], P[2]))
        corresponding_ind.append(corresponding_p_ind)
    return corresponding_ind, np.array(pts_3D), validVec


def normalize(pts, focal, pp):
    # transform pixels into normalized pixels using the focal length and principle point
    a = pts - pp
    return (pts - pp) / focal


def unnormalize(pts, focal, pp):
    # transform normalized pixels into pixels using the focal length and principle point
    return pts * focal + pp


def decompose(EM):
    # extract R, foe and tZ from the Ego Motion
    R = EM[:3, :3]
    t = EM[:3, 3]
    foe = [t[0] / t[2], t[1] / t[2]]
    return R, foe, t[2]


def rotate(pts, R):
    # rotate the points - pts using R
    new_pts = (np.append(pts, np.ones((len(pts), 1)), axis=1)).T
    # new_pts_t = (np.append(pts, [[1], [1], [1]], axis=1)).T
    rot = (np.dot(R, new_pts)).T
    arr = []
    # for i in new_pts:
    #     arr += [np.dot(R, np.array(i).T)]
    for line in rot:
        arr += [[line[0] / line[2], line[1] / line[2]]]
    return np.array(arr)



def find_corresponding_points(p, norm_pts_rot, foe):
    # compute the epipolar line between p and foe
    # run over all norm_pts_rot and find the one closest to the epipolar line
    # return the closest point and its index
    m = (foe[1] - p[1]) / (foe[0] - p[0])
    n = ((p[1] * foe[0]) - (p[0] * foe[1])) / (foe[0] - p[0])
    min_dis = abs((m * norm_pts_rot[0][0] + n - norm_pts_rot[0][1]) / math.sqrt(m * m + 1))
    min_point = norm_pts_rot[0]
    index = 0
    for point, i in zip(norm_pts_rot, range(len(norm_pts_rot))):
        dist = abs((m * point[0] + n - point[1]) / math.sqrt(m * m + 1))
        if dist < min_dis:
            min_dis = dist
            min_point = point
            index = i
    return index, min_point


def calc_dist(p_curr, p_rot, foe, tZ):
    # calculate the distance of p_curr using x_curr, x_rot, foe_x and tZ
    # calculate the distance of p_curr using y_curr, y_rot, foe_y and tZ
    # combine the two estimations and return estimated Z
    z_x = (tZ * (foe[0] - p_rot[0])) / (p_curr[0] - p_rot[0])
    z_y = (tZ * (foe[1] - p_rot[1])) / (p_curr[1] - p_rot[1])
    ratio = abs(p_curr[1] - p_rot[1]) / abs(p_curr[0] - p_rot[0])
    if ratio < 1:
        return ratio * z_y + (1 - ratio) * z_x
    ratio = abs(p_curr[0] - p_rot[0]) / abs(p_curr[1] - p_rot[1])
    return ratio * z_x + (1 - ratio) * z_y


class FrameContainer(object):
    def __init__(self, img):
        self.img = np.asarray(img)
        self.traffic_light = []
        # self.green_traffic_light = []
        self.traffic_lights_3d_location = []
        self.EM = []
        self.corresponding_ind = []
        self.valid = []