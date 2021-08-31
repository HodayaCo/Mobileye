import numpy as np

from model import part3_SFM
from model.part3_SFM import FrameContainer


def part_3(previous_img, current_img, previous_red_points, previous_green_points,
           current_red_points, current_green_points, focal, pp, EM):
    """A function that receive the previous image and the traffic light points in this image and the current image and
    the traffic light points in this image"""

    prev_container = FrameContainer(previous_img)
    curr_container = FrameContainer(current_img)
    curr_container.EM = EM

    # prev_container.red_traffic_light = np.array(previous_red_points)
    # prev_container.green_traffic_light = np.array(previous_green_points)

    prev_container.traffic_light = np.array(previous_red_points + previous_green_points)

    # curr_container.red_traffic_light = np.array(current_red_points)
    # curr_container.green_traffic_light = np.array(current_green_points)

    curr_container.traffic_light = np.array(current_red_points + current_green_points)

    curr_container = part3_SFM.calc_TFL_dist(prev_container, curr_container, focal, pp)

    return curr_container.traffic_lights_3d_location, curr_container.valid, curr_container.traffic_light
