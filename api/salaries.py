from flask import Flask, request, jsonify, Blueprint
from flask_restful import Api, Resource
from __init__ import app, db, cors
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from model.reviews import Review
# from auth_middleware import token_required


salaries_api = Blueprint('salaries_api', __name__, url_prefix='/api/salaries')

# API docs https://flask-restful.readthedocs.io/en/latest/api.html
api = Api(salaries_api)


# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///reviews.db'
# db = SQLAlchemy(app)

class salariesAPI:        
    class _CRUD(Resource):  # User API operation for Create, Read.  THe Update, Delete methods need to be implemeented
        
        def post(self): # Create method
            ''' Read data for json body '''
            body = request.get_json()
            
            survey = body.get('survey')
            salaries = body.get('salaries')
            
            salaries = salaries(
                        salaries=salaries,
                        survey=survey,
                        )
            salaries = salaries.create()
            # success returns json of user
            if salaries:
                return jsonify(salaries.read())

            # failure returns error
            return {'message': f'Error processing request'}, 400

        # this method is when users click on specific job(say "IT Help"), and it will return information about it
        def get(self): # Read Method
            
                salaries = salaries.query.all()    # read/extract all users from database
                json_ready = [salaries.read() for review in reviews]  # prepare output in json
                return jsonify(json_ready) # jsonify creates Flask response object, more specific to APIs than json.dump 
            
    # building RESTapi endpoint
    api.add_resource(_CRUD, '/')