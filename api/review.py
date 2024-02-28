from flask import Flask, request, jsonify, Blueprint
from flask_restful import Api, Resource
from __init__ import app, db, token_required
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from model.reviews import Review


review_api = Blueprint('review_api', __name__, url_prefix='/api/review')

# API docs https://flask-restful.readthedocs.io/en/latest/api.html
api = Api(review_api)


# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///reviews.db'
# db = SQLAlchemy(app)


class ReviewAPI:        
    class _CRUD(Resource):  # User API operation for Create, Read.  THe Update, Delete methods need to be implemeented
        @token_required("Employer")
        def post(self, current_user): # Create method
            ''' Read data for json body '''
            body = request.get_json()
            
            ''' Avoid garbage in, error checking '''
            # validate name
            rating = body.get('rating')
            comment = body.get('comment')
            userid = request.args.get("userid")
            
            ''' #1: Key code block, setup USER OBJECT '''
            re = Review(user_id=userid,
                        rating = rating, 
                      comment=comment)


            ''' #2: Key Code block to add user to database '''
            # create user in database
            Review = re.create(rating)
            # success returns json of user
            if Review:
                return jsonify()

            # failure returns error
            return {'message': f'Processed {rating}, either a format error or User ID {comment} is duplicate'}, 400

        # this method is when users click on specific job(say "IT Help"), and it will return information about it
        def get(self): # Read Method
            
    
            query_params = request.args.get('id')
            if 'id' in query_params:
                query_id = query_params['id'][0]
                print('query_id')
                print(query_id)
                Review = Review.query.filter_by(id=query_id).first()
                if Review:
                    return Review.read()
                else:
                    return {'message': 'Job not found'}, 404
            else:
                reviews = Review.query.all()    # read/extract all users from database
                json_ready = [review.read() for review in reviews]  # prepare output in json
                return jsonify(json_ready) # jsonify creates Flask response object, more specific to APIs than json.dump 
            
    # building RESTapi endpoint
    api.add_resource(_CRUD, '/')

    