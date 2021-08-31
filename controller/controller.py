from controller.tfl_man import TFL_Man
from model.pls_data import PlsData


def init(pls_file_path: str) -> PlsData:
    pls_file = open(pls_file_path, "r")
    lines = pls_file.readlines()
    data = PlsData(lines[0][: -1], int(lines[1][: -1]), [line[:-1] for line in lines[2:]])
    return data


def run(pls_file_path: str):
    pls_data = init(pls_file_path)
    previous_frame = None
    for frame, index in zip(pls_data.lst_frames, range(len(pls_data.lst_frames))):
        previous_frame = TFL_Man.run_frame(index, frame, previous_frame, pls_data)




