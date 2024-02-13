import json, jwt
from flask import Blueprint, request, jsonify, current_app, Response
from flask_restful import Api, Resource # used for REST API building
from datetime import datetime
from auth_middleware import token_required
from model.users import JobUsers, Job

import random
from __init__ import app, db, cors
import flask

from urllib import parse
from urllib.parse import urlparse
from urllib.parse import parse_qs
 
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, select 
from sqlalchemy.ext.declarative import declarative_base 
from sqlalchemy.orm import relationship 
from sqlalchemy.orm import sessionmaker 

jobuser_api = Blueprint('jobuser_api', __name__,
                   url_prefix='/api/jobuser')

# API docs https://flask-restful.readthedocs.io/en/latest/api.html
api = Api(jobuser_api)

@app.before_request
def before_request():
    # Check if the request came from a specific origin
    allowed_origin = request.headers.get('Origin')
    if allowed_origin in ['http://localhost:4100', 'http://127.0.0.1:4100', 'https://nighthawkcoders.github.io', 'http://127.0.0.1:4100/individual/login/', 'http://127.0.0.1:4100/individual/', 'http://127.0.0.1:4100/individualfrontend/login/'
                          , 'http://127.0.0.1:4100/individualfrontend/']:
        cors._origins = allowed_origin

class JobAPI:        
    class _CRUD(Resource):  # User API operation for Create, Read.  THe Update, Delete methods need to be implemeented
    
        def post(self): # Create method
            ''' Read data for json body '''
            body = request.get_json()
            
            ''' Avoid garbage in, error checking '''
            # validate name
            #title = body.get('title')
            #description = body.get('description')
            #qualification = body.get('qualification')
            #pay = body.get('pay')
            #field = body.get('field')
            #location = body.get('location')
            jobid = body.get('jobid')
            userid = body.get('userid')
    
            ''' #1: Key code block, setup USER OBJECT '''
            juo = JobUsers(jobid=jobid,
                          userid=userid)


            ''' #2: Key Code block to add user to database '''
            # create user in database
            jobuser = juo.create()
            # success returns json of user
            if jobuser:
                return jsonify(juo.read())

            # failure returns error
            return {'message': f'Processed {juo}, either a format error or User ID {userid} is duplicate'}, 400

   
        def get(self): # Read Method
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
                jobs = Job.query.all()    # read/extract all users from database
                json_ready = [job.read() for job in jobs]  # prepare output in json
                return jsonify(json_ready) # jsonify creates Flask response object, more specific to APIs than json.dumps
    
    class _Profile(Resource):
        def post(self): # Read Method
           # Session = sessionmaker(bind=engine) 
           # session = Session() 
       
            body = request.get_json()
            userid = body.get('userid')
            #users = JobUsers.query.filter_by(_userid=userid)
            #session.query(JobUsers, Job).filter(Job.id == JobUsers.jobid).all()
            #stmt = select(Job.id, Job.title).select_from( 
            #Job)
  
            #results = session.execute(stmt) 
            #for row in results: 
            #    print(row) 
                
            q = db.session.query(JobUsers, Job).filter(Job.id == JobUsers.jobid).all()
            print('testsetestst')
            print(q)
            
            result = []
            for job in q:
                result.append({
                    'job_id': job.jobs_id,
                })

            return jsonify(result)                    
        
    
    
            
    # building RESTapi endpoint
    api.add_resource(_CRUD, '/')
    api.add_resource(_Profile, '/profile')
    