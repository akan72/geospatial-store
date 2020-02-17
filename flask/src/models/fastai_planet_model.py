import pickle
from fastai.vision import open_image
from flask import session
from src.app import app

def predict_landcover_type() -> str:
    """

    https://docs.fast.ai/vision.image.html

    Returns:
        A string label resulting from the combination of these land cover types:
         {'agriculture', 'artisinal_mine', 'bare_ground', 'blooming', 'blow_down',
          'clear', 'cloudy', 'conventional_mine', 'cultivation',
          'habitation', 'haze', 'partly_cloudy', 'primary', 'road',
          'selective_logging', 'slash_burn', 'water'}
    """

    model = pickle.load(open('models/fastai_planet_model.pkl', 'rb')
    
    # Single image uploading 
    # img = open_image(os.path.join(app.config['UPLOAD_FOLDER'], filename))