from . import db

class Prediction(db.Model):
    pred_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(50), nullable=False)
    time = db.Column(db.DateTime, nullable=False)
    image_path = db.Column(db.String(50), nullable=True)
    model_type = db.Column(db.String(50), nullable=False)
    model_result = db.Column(db.PickleType, nullable=False)
