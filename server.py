from flask import Flask, url_for, send_from_directory, request, jsonify
import logging
import zipfile
import os
from image.process import process_image
from werkzeug.utils import secure_filename
import shutil

app = Flask(__name__)
file_handler = logging.FileHandler('server.log')
app.logger.addHandler(file_handler)
app.logger.setLevel(logging.INFO)

ALLOWED_EXTENSIONS = set(['zip'])
BULK_UPLOAD_FOLDER = os.path.dirname(os.path.realpath(__file__)) + "/tmp/"


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/fake')
def fake():
    test_seal_name = 'LF3-TEST'
    img_path = 'test/images/LF3-80.jpeg'
    return jsonify(process_image(app, test_seal_name, img_path))


@app.route('/training/upload-image', methods=['POST'])
def upload_image():
    app.logger.info(PROJECT_HOME)
    if request.method == 'POST' and request.files['image']:

        # Get name of seal
        seal_name = 'LF1'
        img_to_upload = request.files['image']
        return process_image(app, seal_name, img_to_upload)
    else:
        return "Where is the image?"


@app.route('/training/bulk-upload', methods=['POST'])
def bulk_upload_image():
    data = {}
    if request.method == 'POST':
        seal = request.form['seal']

        if seal == '':
            return "A seal ID is required to submit the zipfile"

        # check if the post request has the file part
        if 'file' not in request.files:
            return "Where is the file?"

        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            return "The filename is empty"
        if file and allowed_file(file.filename):

            file_path = 'tmp/files/'
            directory = os.path.dirname(file_path)
            if os.path.exists(directory):
                shutil.rmtree(file_path)
            os.makedirs(directory)

            extracted_files_dir = BULK_UPLOAD_FOLDER + "/files/"
            filename = secure_filename(file.filename)
            file.save(os.path.join(BULK_UPLOAD_FOLDER, filename))
            zip_ref = zipfile.ZipFile(
                os.path.join(BULK_UPLOAD_FOLDER, filename), 'r')
            zip_ref.extractall(extracted_files_dir)
            zip_ref.close()

            processed_images = 0
            for filename in os.listdir(extracted_files_dir):
                if filename.endswith(".jpeg") or filename.endswith(".png") or filename.endswith(".jpg"):
                    img_path = os.path.join(directory, filename)
                    process_image(app, seal, img_path)
                    processed_images += 1
                    continue
                else:
                    continue

            shutil.rmtree(file_path)

    return {"seal": request.form['seal'], "processed_images": processed_images}


@app.route('/training/zip', methods=['POST'])
def zip_upload_image():

    if request.method == 'POST':

        # check if the post request has the file part
        if 'file' not in request.files:
            return "Where is the file?"

        file = request.files['file']

        if file.filename == '':
            return "The filename is empty"

        if file and allowed_file(file.filename):

            file_path = 'tmp/zip-files/'
            directory = os.path.dirname(file_path)

            if os.path.exists(directory) == False:
                os.makedirs(directory)

            filename = secure_filename(file.filename)
            file.save(os.path.join(file_path, filename))

    return "Done"


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
