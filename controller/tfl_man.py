import numpy as np
from PIL import Image

from model.part_1 import part_1
from model.part_2 import part_2
from model.part_3 import part_3
from model.pls_data import PlsData

from model.frame import Frame
from view.visualize import visualize


class TFL_Man:
    @classmethod
    def run_frame(cls, frame_index: int, frame_path: str, previous_frame: Frame, pls_data: PlsData):

        current_img = Image.open(frame_path)
        red_points_1, green_points_1 = part_1(current_img)
        red_points_2, green_points_2 = part_2(red_points_1, green_points_1, current_img)
        assert (len(red_points_1) >= len(red_points_2) and len(green_points_1) >= len(green_points_2))
        if previous_frame:

            EM = np.eye(4)
            for i in range(frame_index - 1, frame_index):
                EM = np.dot(pls_data.data['egomotion_' + str(i) + '-' + str(i + 1)], EM)

            dist, valid, traffic_light = part_3(previous_frame.frame_img, current_img, previous_frame.red_points,
                                         previous_frame.green_points, red_points_2, green_points_2, pls_data.focal,
                                         pls_data.pp, EM)

        current_frame = Frame(current_img, red_points_2, green_points_2)
        if previous_frame:
            visualize(red_points_1, green_points_1, current_frame, previous_frame, dist, valid, traffic_light)
        else:
            visualize(red_points_1, green_points_1, current_frame,previous_frame)
        return current_frame
