import itertools

try:
    import os
    import json
    import glob
    import argparse

    import numpy as np
    from scipy import signal as sg
    from scipy.ndimage.filters import maximum_filter

    from PIL import Image

    import matplotlib.pyplot as plt
except ImportError:
    print("Need to fix the installation")
    raise


def find_tfl_lights(c_image: Image, **kwargs):
    """
    Detect candidates for TFL lights. Use c_image, kwargs and you imagination to implement
    :param c_image: The image itself as np.uint8, shape of (H, W, 3)
    :param kwargs: Whatever config you want to pass in here
    :return: 4-tuple of x_red, y_red, x_green, y_green
    """
    c_image = np.asarray(c_image)
    imgRed = c_image[:, :, 0]
    imgGreen = c_image[:, :, 1]
    # plt.imshow(imgRed)
    # plt.show(block=True)

    # kernel_3 = np.array([[0, 0.01, 0],
    #                     [0.01, 0.96, 0.01],
    #                     [0, 0.01, 0]])

    kernel_5 = np.array([[-0.065, -0.065, -0.065, -0.065, -0.065],
                         [-0.065, 0.05, 0.4, 0.05, -0.065],
                         [-0.065, 0.4, 0.4, 0.4, -0.065],
                         [-0.065, 0.05, 0.4, 0.05, -0.065],
                         [-0.065, -0.065, -0.065, -0.065, -0.065]])


    kernel_7 = np.array([[-0.07, -0.07, -0.07, -0.07, -0.07, -0.07, -0.07],
                        [-0.07, -0.06,   -0.06, -0.06,  -0.06,  -0.06, -0.07],
                         [-0.07, -0.06,  0.12,   0.5,    0.012,   -0.06, -0.07],
                         [-0.07, -0.06,  0.5,    0.5,    0.5,    -0.06, -0.07],
                         [-0.07, -0.06,  0.012,   0.5,    0.12,   -0.06, -0.07],
                         [-0.07, -0.06,  -0.06,  -0.06,  -0.06,  -0.06,  -0.07],
                         [-0.07, -0.07, -0.07, -0.07, -0.07, -0.07, -0.07]])

    red_conv = sg.convolve(imgRed, kernel_5, mode='same')
    green_conv = sg.convolve(imgGreen, kernel_5, mode='same')

    red_max_flt = maximum_filter(red_conv, size=100)
    red_max_flt[red_max_flt < 200] = float('inf')

    green_max_flt = maximum_filter(green_conv, size=100)
    green_max_flt[green_max_flt < 200] = float('inf')

    red_points = np.subtract(red_max_flt, red_conv)
    green_points = np.subtract(green_max_flt, green_conv)

    red_same_points = np.argwhere(red_points == 0)
    green_same_points = np.argwhere(green_points == 0)
    red_points = []
    green_points = []
    points = list(red_same_points.tolist()) + list(green_same_points.tolist())
    points.sort()
    new_points = list(k for k, _ in itertools.groupby(points))
    for i in new_points:
        if c_image[i[0]][i[1]][1] > c_image[i[0]][i[1]][0]:
            green_points += [[i[1], i[0]]]
        else:
            red_points += [[i[1], i[0]]]
    return red_points, green_points


# GIVEN CODE TO TEST YOUR IMPLENTATION AND PLOT THE PICTURES
def show_image_and_gt(image, objs, fig_num=None):
    plt.figure(fig_num).clf()
    plt.imshow(image)
    labels = set()
    if objs is not None:
        for o in objs:
            poly = np.array(o['polygon'])[list(np.arange(len(o['polygon']))) + [0]]
            plt.plot(poly[:, 0], poly[:, 1], 'r', label=o['label'])
            labels.add(o['label'])
        if len(labels) > 1:
            plt.legend()


def test_find_tfl_lights(image_path, json_path=None, fig_num=None):
    """
    Run the attention code
    """
    image = np.array(Image.open(image_path))
    if json_path is None:
        objects = None
    else:
        gt_data = json.load(open(json_path))
        what = ['traffic light']
        objects = [o for o in gt_data['objects'] if o['label'] in what]

    show_image_and_gt(image, objects, fig_num)

    red_x, red_y, green_x, green_y = find_tfl_lights(image)
    # plt.plot([item[0] for item in red_p], [item[1] for item in red_p], 'rx', markersize=2)
    # plt.plot([item[0] for item in green_p], [item[1] for item in green_p], 'g+', markersize=2)

    plt.plot(red_x, red_y, 'rx', markersize=4)
    plt.plot(green_x, green_y, 'g+', markersize=4)
    plt.show(block=True)


def main(argv=None):
    """It's nice to have a standalone tester for the algorithm.
    Consider looping over some images from here, so you can manually exmine the results
    Keep this functionality even after you have all system running, because you sometime want to debug/improve a module
    :param argv: In case you want to programmatically run this"""

    parser = argparse.ArgumentParser("Test TFL attention mechanism")
    parser.add_argument('-i', '--image', type=str, help='Path to an image')
    parser.add_argument("-j", "--json", type=str, help="Path to json GT for comparison")
    parser.add_argument('-d', '--dir', type=str, help='Directory to scan images in')
    args = parser.parse_args(argv)
    default_base = r'C:\Mbileye\data\images'

    if args.dir is None:
        args.dir = default_base
    flist = glob.glob(os.path.join(args.dir, '*_leftImg8bit.png'))

    for image in flist:
        json_fn = image.replace('_leftImg8bit.png', '_gtFine_polygons.json')

        if not os.path.exists(json_fn):
            json_fn = None
        test_find_tfl_lights(image, json_fn)

    if len(flist):
        print("You should now see some images, with the ground truth marked on them. Close all to quit.")
    else:
        print("Bad configuration?? Didn't find any picture to show")


if __name__ == '__main__':
    main()
