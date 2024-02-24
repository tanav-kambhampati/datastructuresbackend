import json, jwt
from flask import Blueprint, request, jsonify, current_app, Response
from flask_restful import Api, Resource # used for REST API building
from datetime import datetime
from auth_middleware import token_required
from model.users import User
import random
from __init__ import app, db, cors
import flask
from model.jobs import Job
from urllib import parse
from urllib.parse import urlparse
from urllib.parse import parse_qs
job_api = Blueprint('job_api', __name__,
                   url_prefix='/api/job')

# API docs https://flask-restful.readthedocs.io/en/latest/api.html
api = Api(job_api)


@app.before_request
def before_request():
    # Check if the request came from a specific origin
    allowed_origin = request.headers.get('Origin')
    if allowed_origin in ['http://127.0.0.1:4100/joblyFrontend/', 'http://localhost:4100/joblyFrontend/', 'https://aidanlau10.github.io/joblyFrontend/', 
                          'https://aidanlau10.github.io/', 'http://127.0.0.1:4100/joblyFrontend/jobs/', 'http://localhost:4100/joblyFrontend/jobs/',
                          'https://aidanlau10.github.io/joblyFrontend/jobs/']:
        cors._origins = allowed_origin


class JobAPI:        
    class _CRUD(Resource):  # User API operation for Create, Read.  THe Update, Delete methods need to be implemeented
        @token_required("Employer")
        def post(self, current_user): # Create method
            ''' Read data for json body '''
            body = request.get_json()
            
            ''' Avoid garbage in, error checking '''
            # validate name
            title = body.get('title')
            description = body.get('description')
            qualification = body.get('qualification')
            pay = body.get('pay')
            field = body.get('field')
            location = body.get('location')
    
            ''' #1: Key code block, setup USER OBJECT '''
            uo = Job(title=title, 
                      description=description,
                      qualification=qualification,
                      pay=pay,
                      field=field,
                      location=location)


            ''' #2: Key Code block to add user to database '''
            # create user in database
            user = uo.create()
            # success returns json of user
            if user:
                return jsonify(title)

            # failure returns error
            return {'message': f'Processed {title}, either a format error or User ID {description} is duplicate'}, 400

        # this method is when users click on specific job(say "IT Help"), and it will return information about it
        def get(self): # Read Method
            '''
            print(request.url)
            frontendrequest = request.url
            parsed_url = urlparse(frontendrequest)
            print("parsed_url")
            print(parsed_url)
            query_params = parse_qs(parsed_url.query)
            if 'id' in query_params:
                query_id = query_params['id'][0]
                print('query_id')
                print(query_id)
                job = Job.query.filter_by(id=query_id).first()
                if job:
                    return job.read()
                else:
                    return {'message': 'Job not found'}, 404
            else:
            '''
            jobs = Job.query.all()    # read/extract all users from database
            json_ready = [job.read() for job in jobs]  # prepare output in json
            return jsonify(json_ready) # jsonify creates Flask response object, more specific to APIs than json.dumps

                    
        @token_required("Employer")
        def delete(self, _): # Delete Method
            body = request.get_json()
            uid = body.get('uid')
            user = User.query.filter_by(_uid=uid).first()
            if user is None:
                return {'message': f'User {uid} not found'}, 404
            json = user.read()
            user.delete() 
            # 204 is the status code for delete with no json response
            return f"Deleted user: {json}", 204 # use 200 to test with Postman
            
    
    class _Security(Resource):
        @token_required("Employer")
        def get(self):
            return jsonify('authorized')
        def post(self):
            try:
                body = request.get_json()
                if not body:
                    return {
                        "message": "Please provide user details",
                        "data": None,
                        "error": "Bad request"
                    }, 400
                ''' Get Data '''
                uid = body.get('uid')
                if uid is None:
                    return {'message': f'User ID is missing'}, 400
                password = body.get('password')
                
                ''' Find user '''
                user = User.query.filter_by(_uid=uid).first()
                if user is None or not user.is_password(password):
                    return {'message': f"Invalid user id or password"}, 400
                if user:
                    try:
                        token = jwt.encode(
                            {"_uid": user._uid,
                            "role": user.role},
                            current_app.config["SECRET_KEY"],
                            algorithm="HS256"
                        )
                        
                        resp = jsonify({'message': f"Authentication for %s successful" % (user._uid)})
                        resp.set_cookie("test", {"_uid": user._uid},
                                        max_age=3600,
                                secure=True,
                                httponly=True,
                                path='/',
                                samesite='None')
                        resp.set_cookie("jwt", token,
                                max_age=3600,
                                secure=True,
                                httponly=True,
                                path='/',
                                samesite='None'  # This is the key part for cross-site requests

                                # domain="frontend.com"
                                )
                        return resp
                    except Exception as e:
                        return {
                            "error": "Something went wrong",
                            "message": str(e)
                        }, 500
                return {
                    "message": "Error fetching auth token!",
                    "data": None,
                    "error": "Unauthorized"
                }, 404
            except Exception as e:
                return {
                        "message": "Something went wrong!",
                        "error": str(e),
                        "data": None
                }, 500

            
    # building RESTapi endpoint
    api.add_resource(_CRUD, '/')
    api.add_resource(_Security, '/authenticate')
    