from . import db

class PlanetPrediction(db.Model):
    userID = db.Column(db.String(50), primary_key=True)
    time = db.Column(db.DateTime, nullable=False)
    modelType = db.Column(db.String(50), nullable=False)
    image = db.Column(db.String(50), nullable=False)
    result = db.Column(db.PickleType)
