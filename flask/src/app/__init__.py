from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'src/app/static/uploads/'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

from src.app import views
