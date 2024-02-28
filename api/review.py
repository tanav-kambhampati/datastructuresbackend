from flask import Flask, request, jsonify, Blueprint
from flask_restful import Api, Resource
from __init__ import app, db
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from model.reviews import Review
# from auth_middleware import token_required


review_api = Blueprint('review_api', __name__, url_prefix='/api/review')

# API docs https://flask-restful.readthedocs.io/en/latest/api.html
api = Api(review_api)

@app.before_request
def before_request():
    # Check if the request came from a specific origin
    allowed_origin = request.headers.get('Origin')
    if allowed_origin in ['http://127.0.0.1:4100/joblyFrontend/', 'http://localhost:4100/joblyFrontend/', 'https://aidanlau10.github.io/joblyFrontend/', 
                          'https://aidanlau10.github.io/', 'http://127.0.0.1:4100/joblyFrontend/jobs/', 'http://localhost:4100/joblyFrontend/jobs/',
                          'https://aidanlau10.github.io/joblyFrontend/jobs/', 'http://127.0.0.1:4100']:
        cors._origins = allowed_origin
# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///reviews.db'
# db = SQLAlchemy(app)


class ReviewAPI:        
    class _CRUD(Resource):  # User API operation for Create, Read.  THe Update, Delete methods need to be implemeented
        
        def post(self): # Create method
            ''' Read data for json body '''
            body = request.get_json()
            
            ''' Avoid garbage in, error checking '''
            # validate name
            rating = body.get('rating')
            comment = body.get('comment')
            userid = request.args.get("userid")
            
            ''' #1: Key code block, setup USER OBJECT '''
            re = Review(userid=userid,
                        rating=rating,
                        comment=comment
                        )


            ''' #2: Key Code block to add user to database '''
            # create user in database
            review = re.create()
            # success returns json of user
            if review:
                return jsonify(review.read())

            # failure returns error
            return {'message': f'Processed {rating}, either a format error or User ID {comment} is duplicate'}, 400

        # this method is when users click on specific job(say "IT Help"), and it will return information about it
        def get(self): # Read Method
            
                reviews = Review.query.all()    # read/extract all users from database
                json_ready = [review.read() for review in reviews]  # prepare output in json
                return jsonify(json_ready) # jsonify creates Flask response object, more specific to APIs than json.dump 
            
    # building RESTapi endpoint
    api.add_resource(_CRUD, '/')

    