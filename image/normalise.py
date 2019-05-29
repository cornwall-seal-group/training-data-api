from PIL import ImageOps, ImageFilter


def normalise_image(img):
    ac_img = ImageOps.autocontrast(img, cutoff=0.4)

    # Apply increased edge enhancement filter
    return ac_img.filter(ImageFilter.EDGE_ENHANCE_MORE)
