from flask import Flask, request, jsonify
from flask_uploads import UploadSet, configure_uploads, IMAGES
from flask_cors import CORS
from os import listdir
from os.path import isfile, join
import cv2
from graytocolor import GrayToColor as g2c
import datetime
import time

app = Flask(__name__)
CORS(app)

photos = UploadSet('photos', IMAGES)

DEV_URL = 'http://127.0.0.1:5000/'
PHOTO_URL = DEV_URL + 'static/img/'
G2C_PHOTO_URL = DEV_URL + 'static/g2c/'

app.config['UPLOADED_PHOTOS_DEST'] = 'static/img'
app.config['UPLOADED_FILES_URL'] = PHOTO_URL
app.config['UPLOADS_DEFAULT_URL'] = DEV_URL
app.config['UPLOADED_FILES_ALLOW'] = ['jpg', 'png']
configure_uploads(app, photos)

class HttpError(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv


@app.errorhandler(HttpError)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


@app.route('/images/upload', methods=['POST'])
def image_upload():
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
    return get_images()

@app.route('/images', methods=['GET'])
def get_images():
    image_file_names = [f for f in listdir('static/img') if isfile(join('static/img', f))]
    result = list(map(lambda filename: {'file': filename, 'url': PHOTO_URL + filename}, image_file_names))
    return jsonify(result)


@app.route('/colormodeltransform', methods=['POST'])
def color_model_transform():
    color_model = request.json['color_model']
    filename = request.json['filename']
    image = cv2.imread('static/img/' + filename)
    g2c_result = g2c.GrayToColor(image)
    processed_image = g2c_result.getProcessedImage()
        #return jsonify({'file': filename, 'urls': [PHOTO_URL + filename]})
    #raise HttpError('Bad request', status_code=400)
    return 'fk'


@app.route('/intensityslice', methods=['POST'])
def intensity_slice():
    slices = request.json['intensity_slices']
    interval_colors = request.json['interval_colors']
    #return jsonify({'file': filename, 'urls': [PHOTO_URL + filename]})
    return 'fk'


@app.route('/graytocolor', methods=['POST'])
def gray_to_color_transform():
    shift = request.json['phase_shifts']
    filename = request.json['filename']
    image = cv2.imread('static/img/' + filename)
    g2c_result = g2c.GrayToColor(image)
    g2c_result.updateImage({"red": "abs(sin(x/60+{s}))*255".format(s=shift["red"])})
    g2c_result.updateImage({"green": "abs(sin(x/60+{s}))*255".format(s=shift["green"])})
    g2c_result.updateImage({"blue": "abs(sin(x/60+{s}))*255".format(s=shift["blue"])})
    result = g2c_result.getProcessedImage()

    result_filename = create_filename_with_ts(filename)

    cv2.imwrite('static/g2c/' + result_filename, result)
    return jsonify({'file': result_filename, 'urls': [
        G2C_PHOTO_URL + result_filename
    ]})


def create_filename_with_ts(filename):
    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d-%H:%M:%S')
    return st + '-' + filename


@app.route('/smoothensharpen', methods=['POST'])
def smoothen_sharpen():
    model_space = request.json['model_space']
    operation = request.json['operation']
    return 'fk'

