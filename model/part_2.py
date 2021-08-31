from model.part2_test_data import crop_images, predict, get_treshold

def part_2(red_points, green_points, img):
    crops = crop_images(red_points, green_points, img)
    predictions = predict(crops)
    return get_treshold(predictions, crops)


