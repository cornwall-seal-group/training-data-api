from flask import Flask, url_for, send_from_directory, request, jsonify
import logging
import os
import uuid
from predictions.head_detection import get_head_predictions
from PIL import Image

app = Flask(__name__)
file_handler = logging.FileHandler('server.log')
app.logger.addHandler(file_handler)
app.logger.setLevel(logging.INFO)

PROJECT_HOME = os.path.dirname(os.path.realpath(__file__))
UPLOAD_FOLDER = '{}/uploads/'.format(PROJECT_HOME)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
UPLOADS_SUB_FOLDER = 'uploads/'
HEADS_SUB_FOLDER = 'heads/'


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
    img_name = str(uuid.uuid4()) + '.jpg'

    img = Image.open(img_to_upload).convert('RGB')
    saved_path = save_original_image(img_name, img, seal_name)

    app.logger.info('saved image path ' + saved_path)
    head_predictions = get_head_predictions(app, saved_path)

    app.logger.info(head_predictions['predictions'])
    return head_predictions


def save_original_image(img_name, img, seal_name):
    seal_upload_folder = seal_name + '/' + UPLOADS_SUB_FOLDER
    upload_folder = app.config['UPLOAD_FOLDER'] + seal_upload_folder

    app.logger.info(upload_folder)
    create_new_folder(upload_folder)

    saved_path = os.path.join(upload_folder, img_name)
    app.logger.info("saving {}".format(saved_path))
    img.save(saved_path)

    return saved_path


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
