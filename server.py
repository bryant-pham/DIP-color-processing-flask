from flask import Flask, request, jsonify
from flask_uploads import UploadSet, configure_uploads, IMAGES

app = Flask(__name__)

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

@app.route('/upload', methods=['POST'])
def upload():
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        return jsonify({'file': filename, 'url': DEV_PHOTO_URL + filename})
    raise HttpError('Bad request', status_code=400)
