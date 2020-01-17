from flask import request, render_template
import json
import traceback

import src.models.predict_model as predict
from app import app

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/predict', methods=['GET', 'POST'])
def predict_petal_length():
    petal_width = request.args.get('petal_width')

    prediction_results = predict.predict_length(petal_width)
    response = json.dumps(prediction_results[0])

    return response

@app.route('/predict_api', methods=['GET', 'POST'])
def predict_api():
    data = request.get_json()
    petal_width = data['petal_width']

    prediction_results = predict.predict_length(petal_width)
    
    response = json.dumps(prediction_results[0])

    return response