from . import db

class Prediction(db.Model):
    user_id = db.Column(db.String(50), primary_key=True)
    time = db.Column(db.DateTime, nullable=False)
    model_type = db.Column(db.String(50), nullable=False)
    image = db.Column(db.String(50), nullable=True)
    result = db.Column(db.PickleType, nullable=False)
