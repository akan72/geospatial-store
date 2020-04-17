import os
import json
from flask import request, render_template, url_for, send_from_directory, jsonify, Blueprint

from src.app import app
import src.models.iris_model as iris_model
import src.models.planet_model as planet_model

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

# Index
@app.route('/')
def home():
    return render_template('index.html')

### PREDICTIONS 

# Predict petal length within the application
@app.route('/predict', methods=['GET', 'POST'])
def predict_petal_length():
    petal_width = request.args.get('petal_width')

    prediction_results = iris_model.predict_length(petal_width)
    response = json.dumps(prediction_results[0])

    return response

# Predict petal length with a POST request to /predict_api
@app.route('/predict_petal_length_api', methods=['GET', 'POST'])
def predict_petal_length_api():
    data = request.get_json()
    petal_width = data['petal_width']

    prediction_results = iris_model.predict_length(petal_width)
    response = json.dumps(prediction_results[0])

    return response

### FILE UPLOADS

# Function to determine if the filename is valid and the image if a valid type
def allowed_file(filename: str):
    """ Determine if filename is valid.

    Function that determines if an image is valid upload to
    the Flask application given its extension {.png, .jpg, .jpeg}.

    Arguments:
        filename [str]: Path to the filename relative to the extension. 
    
    Returns:
        boolean: True if file extension is valid else false.

    """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Upload the file to our system
@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        files = request.files.getlist('file')

        filenames = []
        results = []
        for file in files:
            name = file.filename
            if allowed_file(name):
                filenames.append(name)

                filepath = os.path.join(app.config['UPLOAD_FOLDER'], name)
                file.save(filepath)

                prediction_results = planet_model.predict_landcover_type(filepath)
                results.append(prediction_results)
        
        content = dict(zip(filenames, results))
        
        return render_template('planet.html', content=content)

    return render_template('file_upload.html')

@app.route('/upload_file_api', methods=['POST'])
def upload_file_api():
    filenames, results = [], []

    for file in request.files.keys():
        file = request.files[file]
        name = file.filename
        if allowed_file(name):
            filenames.append(name)

            filepath = os.path.join(app.config['UPLOAD_FOLDER'], name)
            file.save(filepath)

            prediction_results = planet_model.predict_landcover_type(filepath)
            results.append(prediction_results)
    
    content = dict(zip(filenames, results))

    return jsonify(content)

# Endpoint to serve back the uploaded image within planet.html
@app.route('/data/uploads/<filepath>')
def serve_file(filepath):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename=filepath)
    