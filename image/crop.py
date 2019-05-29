
def crop_image(img, prediction):
    b_box = prediction.bounding_box
    # left, upper, right, lower
    return img.crop(b_box)
