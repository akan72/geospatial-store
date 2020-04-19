from src.app.models import PlanetPrediction
from src.app import db, app

db.create_all(app=app)