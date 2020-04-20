# from flask import Flask

# app = Flask(__name__)
# app.config['UPLOAD_FOLDER'] = 'src/app/static/uploads/'

# from src.app import views

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = 'src/app/static/uploads/'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

db = SQLAlchemy(app)

from src.app import views
from .views import main

app.register_blueprint(main)
