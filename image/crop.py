from PIL import Image


def crop_image(img, prediction):
    b_box = prediction.bounding_box
    # left, upper, right, lower
    return Image.crop(b_box)
