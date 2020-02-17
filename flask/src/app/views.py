from flask import request, render_template, flash, redirect, url_for, Response
import os
import json
from werkzeug.utils import secure_filename

import src.models.iris_model as iris_model
from src.app import app

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

# app.config['UPLOAD_FOLDER'] = os.path.dirname(os.path.realpath(__file__)) + '/../data/uploads' 
app.config['UPLOAD_FOLDER'] = 'data/uploads'

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['GET', 'POST'])
def predict_petal_length():
    petal_width = request.args.get('petal_width')

    prediction_results = iris_model.predict_length(petal_width)
    response = json.dumps(prediction_results[0])

    return response

@app.route('/predict_api', methods=['GET', 'POST'])
def predict_api():
    data = request.get_json()
    petal_width = data['petal_width']

    prediction_results = iris_model.predict_length(petal_width)
    response = json.dumps(prediction_results[0])

    return response

### FILE UPLOADS
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    print(os.path.realpath(__file__))
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            # return redirect(url_for('uploaded_file',
            #                         filename=filename))
            return redirect('/')
    return render_template('file_upload.html')

@app.route('/plotting', methods=['GET'])
def do_plot():
    return render_template('plotting.html')

# Plotting statistics about uploaded imagej
@app.route('/statistics/', methods=['GET'])
def show_statistics():
    pass 
