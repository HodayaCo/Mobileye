class Frame:
    """A class that save image of frame and the traffic lights points"""

    def __init__(self, frame_img, red_points: list, green_points: list):
        self.frame_img = frame_img
        self.red_points = red_points
        self.green_points = green_points