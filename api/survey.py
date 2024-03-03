from flask import request, jsonify, Blueprint
from flask_restful import Api, Resource
from __init__ import app, db, cors
from model.surveys import Survey
from datetime import datetime

survey_api = Blueprint('survey_api', __name__, url_prefix='/api/survey')
api = Api(survey_api)

class SurveyAPI:
    class _CRUD(Resource):
        def post(self):
            ''' Read data for json body '''
            body = request.get_json()
            print(body) 
            
            independent = body['independent']
            artisticTalent = body['artisticTalent']
            communicationSkills = body['communicationSkills']
            fastTyper = body['fastTyper']
            handyPerson = body['handyPerson']
            problemSolving = body['problemSolving']
            showOff = body['showOff']
            teamPlayer = body['teamPlayer']
            jobsuggested = ''
            
            survey = Survey(
                independent=independent,
                artisticTalent=artisticTalent,
                communicationSkills=communicationSkills,
                fastTyper=fastTyper,
                handyPerson = handyPerson,
                problemSolving = problemSolving,
                showOff = showOff,
                teamPlayer = teamPlayer,
                jobsuggested=jobsuggested
                
            )
            survey = survey.create()
            
            if survey:
                return jsonify(survey.read())

            # failure returns error
            return {'message': f'Error processing request'}, 400
            
                
            #job_reco = "Artist"
            
            
            
        def get(self):
            surveys = surveys.query.all()    # read/extract all users from database
            json_ready = [survey.read() for survey in surveys]  # prepare output in json
            return jsonify(json_ready) # j

    # building RESTapi endpoint
    api.add_resource(_CRUD, '/')
