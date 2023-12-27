import json, jwt
from flask import Blueprint, request, jsonify, current_app, Response
from flask_restful import Api, Resource # used for REST API building
from datetime import datetime
from auth_middleware import token_required
from __init__ import app, db
from random import randrange
from datetime import date
import os, base64
import json

from __init__ import app, db
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash

from flask_sqlalchemy import SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)

login_api = Blueprint('login_api', __name__,
                   url_prefix='/api/login')

# API docs https://flask-restful.readthedocs.io/en/latest/api.html
api = Api(login_api)


class Login(db.Model):
    __tablename__ = 'logins'  # table name is plural, class name is singular

    # Define the User schema with "vars" from object
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(db.String(120)))

    def __repr__(self):
        return f"{self.name} - {self.description}"

@login_api.route('/login/')
def get_login():
    logins = Login.query.all()
    
    output = []
    
    for login in logins:
        login_data = {'name': login.name, 'description': login.description}
        output.append(login_data)
    return {"drinks": output}

