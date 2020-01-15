from flask import request, render_template, redirect, url_for
import json
import traceback

import src.models.predict_model as predict
from app import app

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/predict', methods=['GET', 'POST'])
def predict_petal_length():
    if request.args:
        petal_width = request.args.get('petal_width')
        prediction_results = predict.predict_length(petal_width)
        response = json.dumps(prediction_results[0])

        return response
    else: 
        return "No petal_width was passed"

    # try: 
    #     petal_width = request.args.get('petal_width')
    #     prediction_results = predict.predict_length(petal_width)
    #     response = json.dumps(prediction_results[0])

    #     return response
    # except Exception:
    #     return 404