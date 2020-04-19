from flask import Flask

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'src/app/static/uploads/'

from src.app import views