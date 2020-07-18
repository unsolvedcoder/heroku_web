from flask_bootstrap import Bootstrap
from app_helper import *
from camera_settings import *
from detection import *
from flask import Flask, render_template, request, Response, redirect, url_for
from werkzeug.utils import secure_filename
import cv2

import os

__author__ = 'abhijeet'
__source__ = ''

app = Flask(__name__)
bootstrap = Bootstrap(app)
sub = cv2.createBackgroundSubtractorMOG2()

check_settings()
VIDEO = VideoStreaming()

UPLOAD_FOLDER = "C:\\Users\\abhijeet\\PycharmProjects\\Web_App\\static\\uploads"
# DETECTION_FOLDER = "C:\\Users\\abhijeet\\PycharmProjects\\Web_App\\static\\detections"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# app.config['DETECTION_FOLDER'] = DETECTION_FOLDER

@app.route("/uploader", methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['file']
        # create a secure filename
        filename = secure_filename(f.filename)
        print(filename)
        # save file to /static/uploads
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        print(filepath)
        f.save(filepath)
        get_image(filepath, filename)

        return render_template("uploaded.html", display_detection=filename, fname=filename)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/about")
def about():
    return render_template("about.html")


@app.route('/')
def home():
    TITLE = 'Object detection'
    return render_template('index.html', TITLE=TITLE)


@app.route('/video_feed')
def video_feed():
    '''
    Video streaming route.
    '''
    return Response(
        VIDEO.show(), mimetype='multipart/x-mixed-replace; boundary=frame'
    )


# Button requests called from ajax
@app.route('/request_preview_switch')
def request_preview_switch():
    VIDEO.preview = not VIDEO.preview
    print('*' * 10, VIDEO.preview)
    return "nothing"


@app.route('/request_model_switch')
def request_model_switch():
    VIDEO.detect = not VIDEO.detect
    print('*' * 10, VIDEO.detect)
    return "nothing"


@app.route('/request_exposure_down')
def request_exposure_down():
    VIDEO.exposure -= 1
    print('*' * 10, VIDEO.exposure)
    return "nothing"


@app.route('/request_exposure_up')
def request_exposure_up():
    VIDEO.exposure += 1
    print('*' * 10, VIDEO.exposure)
    return "nothing"


@app.route('/request_contrast_down')
def request_contrast_down():
    VIDEO.contrast -= 4
    print('*' * 10, VIDEO.contrast)
    return "nothing"


@app.route('/request_contrast_up')
def request_contrast_up():
    VIDEO.contrast += 4
    print('*' * 10, VIDEO.contrast)
    return "nothing"


@app.route('/reset_camera')
def reset_camera():
    STATUS = reset_settings()
    print('*' * 10, STATUS)
    return "nothing"


if __name__ == '__main__':
    app.run(host='localhost', debug=True, threaded=True)
