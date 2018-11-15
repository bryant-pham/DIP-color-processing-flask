from flask import Flask, request, jsonify
from flask_uploads import UploadSet, configure_uploads, IMAGES
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

photos = UploadSet('photos', IMAGES)

DEV_URL = 'http://127.0.0.1:5000/'
DEV_PHOTO_URL = 'http://127.0.0.1:5000/static/img/'

app.config['UPLOADED_PHOTOS_DEST'] = 'static/img'
app.config['UPLOADED_FILES_URL'] = DEV_PHOTO_URL
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


@app.route('/colormodeltransform', methods=['POST'])
def color_model_transform():
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        model_space = request.form['model_space']
        return jsonify({'file': filename, 'urls': [DEV_PHOTO_URL + filename]})
    raise HttpError('Bad request', status_code=400)


@app.route('/intensityslice', methods=['POST'])
def intensity_slice():
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        slices = request.form['intensity_slices']
        interval_colors = request.form['interval_colors']
        return jsonify({'file': filename, 'urls': [DEV_PHOTO_URL + filename]})
    raise HttpError('Bad request', status_code=400)


@app.route('/graytocolor', methods=['POST'])
def gray_to_color_transform():
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        phase_shifts = request.form['phase_shifts']
        return jsonify({'file': filename, 'urls': [DEV_PHOTO_URL + filename]})
    raise HttpError('Bad request', status_code=400)


@app.route('/smoothensharpen', methods=['POST'])
def smoothen_sharpen():
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        model_space = request.form['model_space']
        operation = request.form['operation']
        return jsonify({'file': filename, 'urls': [DEV_PHOTO_URL + filename]})
    raise HttpError('Bad request', status_code=400)
