# main.py

from flask import Blueprint, render_template, request, send_from_directory
import os, sys
from PIL import Image
import errno
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from tensorflow import keras
import tensorflow as tf
from keras.preprocessing.image import ImageDataGenerator
from os.path import join, dirname, realpath




UPLOAD_FOLDER =  dirname(realpath(__file__)) + '/uploads/mris'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

from os.path import join, dirname, realpath


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


main = Blueprint('main', __name__)


@main.route('/')
def index():
    return render_template('index.html')

@main.route('/predict')
def form():
    return render_template('form.html')

@main.route("/predict", methods=["POST"])
def predict():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'upload' not in request.files:
            flash('No file part')
            return render_template("form.html")
        file = request.files['upload']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            predict_path = dirname(realpath(__file__)) + '/uploads/'
            target_img_shape_1 = 224
            target_img_shape_2 = 224
            predict_datagen = ImageDataGenerator(rescale = 1./255)
            predict_generator = predict_datagen.flow_from_directory(predict_path,target_size = (target_img_shape_1, target_img_shape_2)) 
            reconstructedModel = keras.models.load_model(dirname(realpath(__file__)) + "/model")
            prediction = reconstructedModel.predict(predict_generator)
            mild = round(prediction[0][0]*100, 2)
            moderate = round(prediction[0][1]*100, 2)
            non = round(prediction[0][2]*100, 2)
            veryMild = round(prediction[0][3]*100, 2)
            return render_template("predict.html", mild = mild, moderate = moderate, non = non, veryMild = veryMild)


@main.route('/uploads/<filename>')
def send_file(filename):
    return send_from_directory(UPLOADS_PATH, filename)

@main.route('/profile')
@login_required
def profile():
    return render_template('profile.html', name=current_user.name)
