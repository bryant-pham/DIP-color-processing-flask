from flask import Flask, request, jsonify
from flask_uploads import UploadSet, configure_uploads, IMAGES
from flask_cors import CORS
from os import listdir
from os.path import isfile, join
import cv2
from graytocolor import GrayToColor as g2c
from intensityslice import intensity_slice as int_slice
from ColorspaceConversion import colorSpaceConversion as csc
from smoothensharpen import smoothensharpen as sns
import datetime
import time
import logging

app = Flask(__name__)
CORS(app)

photos = UploadSet('photos', IMAGES)

DEV_URL = 'http://127.0.0.1:5000/'
# DEV_URL = 'http://192.241.234.235:5000/'
PHOTO_URL = DEV_URL + 'static/img/'
G2C_PHOTO_URL = DEV_URL + 'static/g2c/'
CSC_PHOTO_URL = DEV_URL + 'static/csc/'
INTSLICE_PHOTO_URL = DEV_URL + 'static/intslice/'
SS_PHOTO_URL = DEV_URL + 'static/ss/'

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
    image = get_image(filename)
    csc_obj = csc.colorSpaceConversion()
    color_model_arg = 0
    if color_model == 'RGB':
        color_model_arg = 1
    img_result = csc_obj.convertColorSpace(image, color_model_arg)

    if color_model == 'HSI':
        h_filename = create_filename_with_ts(filename, 'H')
        s_filename = create_filename_with_ts(filename, 'S')
        i_filename = create_filename_with_ts(filename, 'I')
        cv2.imwrite('static/csc/' + h_filename, img_result[0])
        cv2.imwrite('static/csc/' + s_filename, img_result[1])
        cv2.imwrite('static/csc/' + i_filename, img_result[2])
        return jsonify({'file': color_model, 'urls': [
            CSC_PHOTO_URL + h_filename,
            CSC_PHOTO_URL + s_filename,
            CSC_PHOTO_URL + i_filename,
        ]})
    else:
        r_filename = create_filename_with_ts(filename, 'R')
        g_filename = create_filename_with_ts(filename, 'G')
        b_filename = create_filename_with_ts(filename, 'B')
        cv2.imwrite('static/csc/' + r_filename, img_result[0])
        cv2.imwrite('static/csc/' + g_filename, img_result[1])
        cv2.imwrite('static/csc/' + b_filename, img_result[2])
        return jsonify({'file': color_model, 'urls': [
            CSC_PHOTO_URL + r_filename,
            CSC_PHOTO_URL + g_filename,
            CSC_PHOTO_URL + b_filename,
        ]})


@app.route('/intensityslice', methods=['POST'])
def intensity_slice():
    slices = request.json['slices']
    interval_colors = request.json['interval_colors']
    filename = request.json['filename']
    image = get_image(filename)
    int_slice_obj = int_slice.IntSlice()
    img_result = int_slice_obj.get_sliced_img(image, slices, interval_colors)
    result_filename = create_filename_with_ts(filename)

    cv2.imwrite('static/intslice/' + result_filename, img_result)
    return jsonify({'file': result_filename, 'urls': [
        INTSLICE_PHOTO_URL + result_filename
    ]})


@app.route('/graytocolor', methods=['POST'])
def gray_to_color_transform():
    shift = request.json['phase_shifts']
    filename = request.json['filename']
    image = get_image(filename)
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


def get_image(filename):
    return cv2.imread('static/img/' + filename)


def create_filename_with_ts(filename, extra=''):
    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d-%H:%M:%S')
    return st + '-' + extra + '-' + filename


@app.route('/smoothensharpen', methods=['POST'])
def smoothen_sharpen():
    filter = request.json['filter']
    filename = request.json['filename']
    filter_args = request.json['args']
    image = get_image(filename)
    sns_obj = sns.SmoothenSharpen(image)
    sns_obj.loadKernel(filter, filter_args)
    sns_obj.applyFilter()
    filtered_bgr = sns_obj.getProcessedBGR()
    filtered_hls = sns_obj.getProcessedHLS()
    filtered_diff = sns_obj.getProcessedDiff()
    bgr_filename = create_filename_with_ts(filename, 'bgr')
    hls_filename = create_filename_with_ts(filename, 'hls')
    diff_filename = create_filename_with_ts(filename, 'diff')
    cv2.imwrite('static/ss/' + bgr_filename, filtered_bgr)
    cv2.imwrite('static/ss/' + hls_filename, filtered_hls)
    cv2.imwrite('static/ss/' + diff_filename, filtered_diff)

    return jsonify({'file': filename, 'urls': [
        SS_PHOTO_URL + bgr_filename,
        SS_PHOTO_URL + hls_filename,
        SS_PHOTO_URL + diff_filename
    ], 'notes': filter})


if __name__ != '__main__':
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)
