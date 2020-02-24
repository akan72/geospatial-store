from typing import List
import os
import pickle
from fastai.vision import open_image, load_learner
from flask import session

def predict_landcover_type(filepath: str) -> List[str]:
    """ Predict the landcover type form a Planet Skysat Image.

    Utilizes the Fasiai.vision land cover classification model in order to predict 
    a set of landcover types from 

    https://docs.fast.ai/vision.image.html

    Args:
        filepath (str): Path to the image that will be run through the model 

    Returns:
        List[str]: A list of string labels resulting from a combination of the following land cover types: 
         {'agriculture', 'artisinal_mine', 'bare_ground', 'blooming', 'blow_down',
          'clear', 'cloudy', 'conventional_mine', 'cultivation',
          'habitation', 'haze', 'partly_cloudy', 'primary', 'road',
          'selective_logging', 'slash_burn', 'water'}

    """
    image = open_image(filepath)

    # model = pickle.load(open('models/fastai_planet_model.pkl', 'rb'))
    model = load_learner('models/', 'fastai_planet_model.pkl')
    print(type(model))

    return model.predict(image)

# Single image uploading 
# img = open_image(os.path.join(app.config['UPLOAD_FOLDER'], filename))
# https://forums.fast.ai/t/how-to-make-predictions-with-vision-learner-solved/34456/9
# https://docs.fast.ai/vision.image.html