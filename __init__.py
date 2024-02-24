from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import os
from flask_cors import CORS
from flask import request

"""
These object can be used throughout project.
1.) Objects from this file can be included in many blueprints
2.) Isolating these object definitions avoids duplication and circular dependencies
"""

# Setup of key Flask object (app)
app = Flask(__name__)

cors = CORS(app, supports_credentials=True, methods=["GET", "POST", "PUT", "DELETE"])
@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', 'http://127.0.0.1:4100/joblyFrontend/')
    allowed_origins = ['http://127.0.0.1:4100/joblyFrontend/', 'http://localhost:4100/joblyFrontend/', 'https://aidanlau10.github.io/joblyFrontend/', 
                          'https://aidanlau10.github.io/', 'http://127.0.0.1:4100/joblyFrontend/jobs/', 'http://localhost:4100/joblyFrontend/jobs/',
                          'https://aidanlau10.github.io/joblyFrontend/jobs/', 'http://127.0.0.1:4100']

    origin = request.headers.get('Origin')
    if origin and origin in allowed_origins:
        response.headers.add('Access-Control-Allow-Origin', origin)

    response.headers.add('Access-Control-Allow-Origin', request.headers.get('Origin'))
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    return response

# Setup SQLAlchemy object and properties for the database (db)
dbURI = 'sqlite:////volumes/sqlite.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = dbURI
SECRET_KEY = os.environ.get('SECRET_KEY') or 'SECRET_KEY'
app.config['SECRET_KEY'] = SECRET_KEY
db = SQLAlchemy()
Migrate(app, db)

# Images storage
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024  # maximum size of uploaded content
app.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.png', '.gif']  # supported file types
app.config['UPLOAD_FOLDER'] = 'volumes/uploads/'  # location of user uploaded content