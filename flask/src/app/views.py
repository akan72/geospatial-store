import os, sys
import json
from flask import request, render_template, url_for, send_from_directory, jsonify, Blueprint

from src.app import app
import src.models.iris_model as iris_model
import src.models.planet_model as planet_model

main = Blueprint('main', __name__)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

# Index
## TODO: Allow users to choose between models
@main.route('/')
def home():
    return render_template('index.html')

### PREDICTIONS 
@main.route('/iris')
def iris():
    return render_template('iris.html')

# Predict petal length with a POST request or within the application form
# TODO: Multiple uploads
@main.route('/predict_petal_length', methods=['GET', 'POST'])
def predict_petal_length():
    error = None
    # Allow for handling of form input, and 
    if request.is_json:
        petal_width = request.get_json()['petal_width']
    else: 
        petal_width = request.values['petal_width']

        prediction_results = iris_model.predict_length(petal_width)
        response = json.dumps(prediction_results[0])

    return jsonify(response)

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
# TODO: Change from index.html
@main.route('/upload_image', methods=['GET', 'POST'])
def upload_image():
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

    return render_template('index.html')

@main.route('/upload_image_api', methods=['GET', 'POST'])
def upload_image_api():
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

# Endpoint to serve back the uploaded image to planet.html
@main.route('/data/uploads/<filepath>')
def serve_file(filepath):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename=filepath)

@main.route('/test')
def test():
    return jsonify({'k1': 'v1', 'k2': 'v2', 'k3': 'v3'})
