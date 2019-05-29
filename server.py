from flask import Flask, url_for, send_from_directory, request, jsonify
import logging
import os
import uuid
from predictions.head_detection import get_head_predictions
from image.crop import crop_image
from image.process import normalise_image
from image_meta.store import store_seal_img_metadata, store_seal_metadata
from PIL import Image

app = Flask(__name__)
file_handler = logging.FileHandler('server.log')
app.logger.addHandler(file_handler)
app.logger.setLevel(logging.INFO)

UPLOAD_FOLDER = '../seal-images/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ORIGINAL_IMG_FOLDER = 'originals/'
HEADS_IMG_FOLDER = 'heads/'


def create_new_folder(local_dir):
    newpath = local_dir
    if not os.path.exists(newpath):
        os.makedirs(newpath)
    return newpath


@app.route('/')
def hello():
    return {"hello": "world"}


@app.route('/fake')
def fake():
    test_seal_name = 'LF3-TEST'
    img_path = 'test/images/LF3-80.jpeg'
    return jsonify(save_image(test_seal_name, img_path))


@app.route('/training/upload-image', methods=['POST'])
def upload_image():
    app.logger.info(PROJECT_HOME)
    if request.method == 'POST' and request.files['image']:

        # Get name of seal
        seal_name = 'LF1'
        # Create folder for seal if not exists
        # Save file to <SEAL>/uploads/ folder
        # Submit image to Azure to find head
        # Crop image, and update contrast, save to <SEAL>/heads/ folder

        img_to_upload = request.files['image']

        return save_image(seal_name, img_to_upload)
    else:
        return "Where is the image?"


def save_image(seal_name, img_to_upload):

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
    seal_folder = app.config['UPLOAD_FOLDER'] + seal_name
    store_seal_img_metadata(seal_folder, seal_name, unique_img_name)

    # Save seal name for reference so we know what seals we have images for
    folder = app.config['UPLOAD_FOLDER']
    store_seal_metadata(folder, seal_name)

    return {
        "percentage": best_prediction.probability,
        "id": unique_img_name
    }


def save_original_image(img_name, img, seal_name):
    seal_upload_folder = seal_name + '/' + ORIGINAL_IMG_FOLDER
    upload_folder = app.config['UPLOAD_FOLDER'] + seal_upload_folder

    app.logger.info(upload_folder)
    create_new_folder(upload_folder)

    saved_path = os.path.join(upload_folder, img_name)
    app.logger.info("saving {}".format(saved_path))
    img.save(saved_path)

    return saved_path


def save_normalised_image(img_name, img, seal_name):
    seal_upload_folder = seal_name + '/' + HEADS_IMG_FOLDER
    upload_folder = app.config['UPLOAD_FOLDER'] + seal_upload_folder

    app.logger.info(upload_folder)
    create_new_folder(upload_folder)

    saved_path = os.path.join(upload_folder, img_name)
    app.logger.info("saving {}".format(saved_path))
    img.save(saved_path)

    return saved_path


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
