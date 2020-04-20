from src.app.models import Prediction
from src.app import db, app

db.create_all(app=app)