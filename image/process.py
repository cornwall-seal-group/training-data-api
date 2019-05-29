from PIL import Image, ImageOps, ImageFilter
from predictions.head_detection import get_head_predictions
import uuid
import os
from image.crop import crop_image
from image.normalise import normalise_image
from image_meta.store import store_seal_img_metadata, store_seal_metadata

UPLOAD_FOLDER = '../seal-images/'
ORIGINAL_IMG_FOLDER = 'originals/'
HEADS_IMG_FOLDER = 'heads/'


def process_image(app, seal_name, img_to_upload):

    # Create a unique filename for the image
    unique_img_name = str(uuid.uuid4())
    img_name = unique_img_name + '.jpg'

    img = Image.open(img_to_upload).convert('RGB')
    saved_path = save_original_image(img_name, img, seal_name)

    app.logger.info('saved image path ' + saved_path)
    head_predictions = get_head_predictions(saved_path)

    best_prediction = head_predictions['best_prediction']
    app.logger.info(best_prediction)

    cropped_img = crop_image(img, best_prediction)
    normalised_img = normalise_image(cropped_img)

    save_normalised_image(img_name, normalised_img, seal_name)

    # Save metadata to file
    seal_folder = UPLOAD_FOLDER + seal_name
    store_seal_img_metadata(seal_folder, seal_name, unique_img_name)

    # Save seal name for reference so we know what seals we have images for
    store_seal_metadata(UPLOAD_FOLDER, seal_name)

    return {
        "best_prediction_percentage": best_prediction.probability,
        "id": unique_img_name
    }


def create_new_folder(local_dir):
    newpath = local_dir
    if not os.path.exists(newpath):
        os.makedirs(newpath)
    return newpath


def save_original_image(img_name, img, seal_name):
    seal_upload_folder = seal_name + '/' + ORIGINAL_IMG_FOLDER
    upload_folder = UPLOAD_FOLDER + seal_upload_folder

    create_new_folder(upload_folder)

    saved_path = os.path.join(upload_folder, img_name)
    img.save(saved_path)

    return saved_path


def save_normalised_image(img_name, img, seal_name):
    seal_upload_folder = seal_name + '/' + HEADS_IMG_FOLDER

    upload_folder = UPLOAD_FOLDER + seal_upload_folder
    create_new_folder(upload_folder)

    saved_path = os.path.join(upload_folder, img_name)
    img.save(saved_path)

    return saved_path
