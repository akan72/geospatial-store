from flask import request, render_template, flash, redirect, url_for, session, send_from_directory
import os
import json
from werkzeug.utils import secure_filename

import src.models.iris_model as iris_model
from src.app import app

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['GET', 'POST'])
def predict_petal_length():
    petal_width = request.args.get('petal_width')

    prediction_results = iris_model.predict_length(petal_width)
    response = json.dumps(prediction_results[0])

    return response

@app.route('/predict_planet', methods=['GET', 'POST'])
def predict_image_type():
    pass
    

@app.route('/predict_api', methods=['GET', 'POST'])
def predict_api():
    data = request.get_json()
    petal_width = data['petal_width']

    prediction_results = iris_model.predict_length(petal_width)
    response = json.dumps(prediction_results[0])

    return

### FILE UPLOADS
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        files = request.files.getlist('file')
        for file in files:
            if allowed_file(file.filename):
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
                return render_template('planet.html', files=files)
    return render_template('file_upload.html')

@app.route('/data/uploads/<filepath>')
def serve_file(filepath):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename=filepath)

@app.route('/plotting', methods=['GET'])
def do_plot():
    return render_template('plotting.html')

# Plotting statistics about uploaded imagej
@app.route('/statistics/', methods=['GET'])
def show_statistics():
    pass 
