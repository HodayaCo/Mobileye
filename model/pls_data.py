import pickle


class PlsData:
    """A class that saved the data from the pls file"""

    def __init__(self, pkl_path: str, first_frame: int, lst_frames: list):
        with open(pkl_path, 'rb') as pklfile:
            self.data = pickle.load(pklfile, encoding='latin1')
        self.focal = self.data['flx']
        self.pp = self.data['principle_point']
        self.first_frame = first_frame
        self.lst_frames = lst_frames
