
def visualize_part3(red_points, green_points, dist, valid, part3_sec, traffic_light):
    part3_sec.plot([item[0] for item in red_points], [item[1] for item in red_points], 'rx', markersize=1)
    part3_sec.plot([item[0] for item in green_points], [item[1] for item in green_points], 'g+', markersize=1)
    for i in range(len(traffic_light)):
        if valid[i]:
            part3_sec.text(traffic_light[i, 0], traffic_light[i, 1], r'{0:.1f}'.format(dist[i, 2]), color='r', fontsize='5')