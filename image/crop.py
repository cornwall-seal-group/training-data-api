
#
# {
#    height: 0.494349241,
#    left: 0.0181922168,
#    top: 0.0303361267,
#    width: 0.4266795,
# }


def crop_image(img, prediction):
    image_width = img.width
    image_height = img.height

    b_box = prediction.bounding_box
    b_height = b_box.height
    b_width = b_box.width
    b_top = b_box.top
    b_left = b_box.left

    left = b_left*image_width
    upper = b_top*image_height
    right = left + (b_width*image_width)
    lower = upper + (b_height*image_height)
    # left, upper, right, lower
    print (left, upper, right, lower)
    return img.crop((left, upper, right, lower))
