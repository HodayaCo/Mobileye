from view.visualize_part1 import visualize_part1
import matplotlib.pyplot as plt

from view.visualize_part2 import visualize_part2
from view.visualize_part3 import visualize_part3


def visualize(red_points_part1, green_points_part1, curr_frame, previous_frame, dist = None, valid = None, traffic_light = None):
    # norm_prev_pts, norm_curr_pts, R, norm_foe, tZ = part3_SFM.prepare_3D_data(prev_container, curr_container, focal, pp)
    # norm_rot_pts = part3_SFM.rotate(norm_prev_pts, R)
    # rot_pts = part3_SFM.unnormalize(norm_rot_pts, focal, pp)
    # foe = np.squeeze(part3_SFM.unnormalize(np.array([norm_foe]), focal, pp))

    fig, (part1_sec, part2_sec, part3_sec) = plt.subplots(3, 1)
    # prev_sec.set_title('prev(' + str(prev_frame_id) + ')')
    part1_sec.imshow(curr_frame.frame_img)
    visualize_part1(red_points_part1, green_points_part1, part1_sec)
    part2_sec.imshow(curr_frame.frame_img)
    visualize_part2(curr_frame.red_points, curr_frame.green_points, part2_sec)
    if previous_frame:
        part3_sec.imshow(curr_frame.frame_img)
        visualize_part3(curr_frame.red_points, curr_frame.green_points, dist, valid, part3_sec, traffic_light)
    # prev_p = prev_container.traffic_light
    # prev_sec.plot(prev_p[:, 0], prev_p[:, 1], 'b+')

    # curr_sec.set_title('curr(' + str(curr_frame_id) + ')')
    # curr_sec.imshow(curr_container.img)
    # curr_p = curr_container.traffic_light
    # curr_sec.plot(curr_p[:, 0], curr_p[:, 1], 'b+')
    #
    # for i in range(len(curr_p)):
    #     curr_sec.plot([curr_p[i, 0], foe[0]], [curr_p[i, 1], foe[1]], 'b')
    #     if curr_container.valid[i]:
    #         curr_sec.text(curr_p[i, 0], curr_p[i, 1],
    #                       r'{0:.1f}'.format(curr_container.traffic_lights_3d_location[i, 2]), color='r')
    # curr_sec.plot(foe[0], foe[1], 'r+')
    # curr_sec.plot(rot_pts[:, 0], rot_pts[:, 1], 'g+')
    plt.show()
