
def visualize_part2(red_points, green_points, part2_sec):
    part2_sec.plot([item[0] for item in red_points], [item[1] for item in red_points], 'rx', markersize=1)
    part2_sec.plot([item[0] for item in green_points], [item[1] for item in green_points], 'g+', markersize=1)