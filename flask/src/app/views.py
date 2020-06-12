import os
import sys
import json
import random
import pickle
import datetime

from numpy import round
from flask import request, render_template, url_for, send_from_directory, jsonify, Blueprint

from src.app import app, db
from src.app.models import Prediction
import src.models.iris_model as iris_model
import src.models.planet_model as planet_model
import src.models.windmill_model as windmill_model

main = Blueprint('main', __name__)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

@main.route('/')
def index():
    return render_template('index.html')

### PREDICTIONS 

@main.route('/iris')
def iris():
    return render_template('iris.html')

@main.route('/predict_petal_length_api', methods=['GET', 'POST'])
@main.route('/predict_petal_length', methods=['GET', 'POST'])
def predict_petal_length():
    """ Predict Petal Length based on Petal Width for the canonical `Iris` dataset

    Allows for input using a form within the application or through a POST request 
    with possibly JSON-encoded input.

    """
    if request.is_json:
        petal_width = request.get_json()['petal_width']
    else: 
        petal_width = request.values['petal_width']

    prediction_results = iris_model.predict_length(petal_width)
    response = json.dumps(prediction_results[0])

    new_prediction = Prediction(
        user_id=random.randint(0, 5),
        model_type='Iris',
        time=datetime.datetime.now(),
        image_path=None,
        model_result=round(prediction_results, 2)
    )
    
    db.session.add(new_prediction)
    db.session.commit()
    
    # If the request path is from the GUI, then render the correct template, return a JSON of model results
    if str(request.path) == '/predict_petal_length':
        content = {petal_width: response}

        return render_template('iris_result.html', content=content)

    return jsonify(response)

### FILE UPLOADS

# Function to determine if the filename is valid and the image if a valid type
def allowed_file(filename: str):
    """Determine if filename is valid.

    Function that determines if an image is valid upload to
    the Flask application given its extension {.png, .jpg, .jpeg}.

    Arguments:
        filename [str]: Path to the filename relative to the extension. 
    
    Returns:
        boolean: True if file extension is valid else false.

    """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@main.route('/upload_image_api', methods=['GET', 'POST'])
@main.route('/upload_image', methods=['GET', 'POST'])
def upload_image():
    """ Upload a Planet Kaggle Amazon image to our application

    """
    # If the API does not receive a POST request, return back to the image upload page
    if request.method == 'POST':
        images, filenames = [], []

        # If the image input is in JSON format, iterate over the keys and save files with valid extensions
        # Takes in images with the encoding 'multipart/form-data' (handled by an HTML form or the `requests` module)
        for file in request.files.getlist('file'):
            name = file.filename

            if allowed_file(name):
                images.append(file)
                filenames.append(name)

        results = []
        # Iterate over all opf the valid files and save to the filesystem
        for file, name in zip(images, filenames):
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], name)
            file.save(filepath)

            # Run the landcover prediction model on the file and save results
            prediction_results = planet_model.predict_landcover_type(filepath)
            results.append(prediction_results)
        
            new_prediction = Prediction(
                user_id=random.randint(0, 5),
                model_type='Planet',
                time=datetime.datetime.now(),
                image_path=name,
                model_result=prediction_results
            )

            db.session.add(new_prediction)
            db.session.commit()

        # Zip together results with file names for storage
        output = dict(zip(filenames, results))

        # If calling the endpoint through the application, render the results page, else just return the predictions
        if str(request.path) == '/upload_image':
            return render_template('image_result.html', content=output)

        return jsonify(output)

    return render_template('image_upload.html')

@main.route('/windmill_api', methods=['GET', 'POST'])
@main.route('/windmill', methods=['GET', 'POST'])
def upload_windmill():
    """ Upload a Windmill image to our application

    """
    # If the API does not receive a POST request, return back to the image upload page
    if request.method == 'POST':
        images, filenames = [], []

        # If the image input is in JSON format, iterate over the keys and save files with valid extensions
        # Takes in images with the encoding 'multipart/form-data' (handled by an HTML form or the `requests` module)
        for file in request.files.getlist('file'):
            name = file.filename

            if allowed_file(name):
                images.append(file)
                filenames.append(name)

        results = []
        
        # Iterate over all opf the valid files and save to the filesystem
        for file, name in zip(images, filenames):
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], name)
            file.save(filepath)

            # Run the landcover prediction model on the file and save results
            prediction_results = windmill_model.predict_windmill_orientation(filepath)
            prediction_results = prediction_results[prediction_results.find('windmills/'):]

            results.append(prediction_results)
        
            new_prediction = Prediction(
                user_id=random.randint(0, 5),
                model_type='Windmill',
                time=datetime.datetime.now(),
                image_path=name,
                model_result=prediction_results
            )

            db.session.add(new_prediction)
            db.session.commit()

        # Zip together results with file names for storage
        output = dict(zip(filenames, results))

        # If calling the endpoint through the application, render the results page, else just return the predictions
        if str(request.path) == '/windmill':
            return render_template('windmill_result.html', content=output)

        return jsonify(output)

    return render_template('windmill_upload.html')

@main.route('/data/processed/<string:filepath>')
def serve_file(filepath):
    print('data'+filepath[5:])
    return send_from_directory('data/', filename=filepath[5:])

### DASHBOARD 

@main.route('/dashboard', methods=['GET', 'POST'])
@main.route('/dashboard/<int:user_id>', methods=['GET', 'POST'])
@main.route('/dashboard/<string:model_type>', methods=['GET', 'POST'])
@main.route('/dashboard/<int:user_id>/<string:model_type>', methods=['GET', 'POST'])
def dashboard(user_id: int = None, model_type: str = None):
    """ Display all model prediction results in a tabular format

    Tables results are sorted by user_id, ascending

    """
    user_id = request.args.get('user_id', default=None)
    model_type = request.args.get('model_type', default=None)

    if user_id and model_type:
        results = Prediction.query.filter_by(user_id=user_id, model_type=model_type)
    elif user_id is not None:
        results = Prediction.query.filter_by(user_id=user_id)
    elif model_type is not None:
        results = Prediction.query.filter_by(model_type=model_type)
    else:
        results = Prediction.query.all()

    content = []
    for result in results:
        record = [result.user_id, result.model_type, result.time.strftime('%m/%d/%Y'), '' if result.image_path is None else result.image_path, result.model_result]
        content.append(record)

    content = sorted(content, key = lambda x: x[0])

    return render_template('dashboard.html', content=content)
