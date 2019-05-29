from flask import Flask, url_for, send_from_directory, request
import logging
import os
import uuid
from training-data-api.azure.head_detection import get_head_predictions
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
    return 'Hello, World'


@app.route('/training/upload-image', methods=['POST'])
def upload_image():
    app.logger.info(PROJECT_HOME)
    if request.method == 'POST' and request.files['image']:

        # Get name of seal
        seal_name = 'LF1'

        # Create a unique filename for the image
        img_name = str(uuid.uuid4()) + '.jpg'

        # Create folder for seal if not exists
        # Save file to <SEAL>/uploads/ folder
        # Submit image to Azure to find head
        # Crop image, and update contrast, save to <SEAL>/heads/ folder

        img_to_upload = request.files['image']
        img = Image.open(img_to_upload).convert('RGB')
        saved_path = save_original_image(img_name, img, seal_name)

        predictions = get_head_predictions(saved_path)

        return predictions
    else:
        return "Where is the image?"


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
