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

    # https://forums.fast.ai/t/how-to-make-predictions-with-vision-learner-solved/34456/9
    model = load_learner('models/', 'fastai_planet_model.pkl')

    category, tensor, probs = model.predict(image)

    return str(category).split(';')

def top_k_predictions(model, probs, k: int):
    """ Returns the top `k` most probable classes from our model 

    After training a fastai Learner on a multi-label classification problem,
    return the label and probabilities associated with the top `k` most 
    probable classes.

    Args:
        model [Learner]: Fastai Learner trained to do multi-label classification
        probs [Tensor]: Tensor of class probabilities
        k [int]: Number of classes/probabilities to return 

    Returns:
        List[str]: Top k classes
        List[tensor]: Probabilities associated with the top k classess

    """
    
    # Determine all the potential classes our model will choose from 
    classes = model.data.classes
    num_classes = len(classes)

    # Limit k to the total number of classes
    if k > num_classes:
        k = num_classes

    # Get the indices of the `k` classes with highest probabilities
    top_k_indices = probs.argsort(descending=True)[:k]

    labels = []
    probabilities = []

    for i in top_k_indices:
        labels.append(classes[i])
        probabilities.append(probs[i])

    return labels, probabilities