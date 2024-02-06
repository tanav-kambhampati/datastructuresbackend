from flask import Blueprint, render_template, redirect, url_for, request, jsonify, make_response
from flask_login import login_required, logout_user, login_user
from functools import wraps
from http import cookies
import bcrypt
from bcrypt import gensalt
from model.users import db
from flask import current_app
from __init__ import app, db, cors
from datetime import datetime, timedelta
import jwt
from model.users import User, db
from flask_restful import Api, Resource
import random

jwt_bp = Blueprint('jwt_auth', __name__,
                   url_prefix='/api/jwt_auth')
# Creating a blueprint for jwt_auth related routes
api = Api(jwt_bp)
   
@app.before_request
def before_request():
    # Check if the request came from a specific origin
    allowed_origin = request.headers.get('Origin')
    if allowed_origin in ['http://localhost:4100', 'http://127.0.0.1:4100', 'https://nighthawkcoders.github.io', 'http://127.0.0.1:4100/cptprojectfrontend/login/', 'http://127.0.0.1:4100/cptprojectfrontend/']:
        cors._origins = allowed_origin
   
    
@jwt_bp.route('/register', methods=['POST'])
def register():
    
   # Getting the request data as json
   data = request.get_json()
   # Checking if the required data (name, password) are present
   if not data or not data.get('name') or not data.get('password'):
       # If not, return a JSON response with a message and a 400 status code
       return jsonify({'message': 'name or password field is empty.'}), 400
   # Querying the User table to check if a user with the provided name already exists
   user = User.query.filter_by(_name=data.get('name')).first()


   # If a user is found, return a JSON response with a message and a 400 status code
   if user:
        return jsonify({'message': 'User already exists. Please Log in.'}), 400


   # If a user was not found, the password is hashed using bcrypt
   hashed_password = bcrypt.hashpw(data.get('password').encode('utf-8'), bcrypt.gensalt()).decode('utf-8')  # ensure the hashed password is in string format
   # A new User object is created with the provided name and hashed password
   UserName = data.get('name')[:4]
   UserId = random(0,100)
   NewUserId = f"{UserName}" + f"{UserId}"
   new_user = User(name=data.get('name'), password=hashed_password, uid=NewUserId)
   # The new User object is added to the db session
   db.session.add(new_user)
   # The db session is committed to save the changes
   db.session.commit()
   # A JSON response is returned with a message and a 201 status code
   return jsonify({'message': 'New user created!'}), 201

@jwt_bp.route('/login', methods=['POST'])
def login():
   # get the name and password from the request
   data = request.get_json()
   uid = data.get('uid')
   password = data.get('password')

   # authenticate the user, for example by checking the name and password against a database
   user = User.query.filter_by(_uid=uid).first()

   # if the user doesn't exist or the password is wrong, return an error
   if user is None:# or not user.check_password(password):
       return jsonify({'message': f'Invalid name or password {name}' }), 400

   # if the user is authenticated, create a JWT token for them
   token = jwt.encode(payload= {'name': user.name}, key=current_app.config['SECRET_KEY'], algorithm="HS256")
   print("Token:", token)

   expires = datetime.now()
   expires = expires + timedelta(days=30) # expires in 30 days
   # set the JWT token in a secure HTTP-only cookie in the response

   response = make_response(jsonify({'message': 'Logged in'}), 200)
   response.set_cookie('token', token, secure=True, samesite='None', path='/', httponly=True)
  
   print(response.headers)
   return response


