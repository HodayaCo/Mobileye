
def visualize_part1(red_points, green_points, part1_sec):
    part1_sec.plot([item[0] for item in red_points], [item[1] for item in red_points], 'rx', markersize=1)
    part1_sec.plot([item[0] for item in green_points], [item[1] for item in green_points], 'g+', markersize=1)