from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource
from model.vehiclesmodel import DecisionTreeClassifier as dt
from model.vehiclesmodel import OneHotEncoder as enc
from sklearn.linear_model import LogisticRegression
import pandas as pd

# Import the FootballScoreModel class

rocketsuccess_api = Blueprint('rocketsuccess_', __name__, url_prefix='/api/rocketsuccess')
api = Api(rocketsuccess_api)

# payload_mass,origin_country,company,engine_strength,success_rate

dt = dt  # Assuming dt is already trained
enc = enc  # Assuming enc is already initialized and fitted
class RocketSucessAPI(Resource):

    def __init__(self):
        rocket_data = pd.read_csv('rocket_launch_data.csv')
        td = rocket_data.copy()

        self.logreg = LogisticRegression(max_iter=1000)
        X = td.drop('success_rate', axis=1)
        y = td['success_rate']
        self.logreg.fit(X, y)

    def predict_rocket_success(payload_mass, company, engine_strength):
        try:
            # Preprocess the input data
            data = pd.DataFrame({'payload_mass': [payload_mass], 'company': [company], 'engine_strength': [engine_strength]})
            encoded_data = enc.transform(data)
            
            # Make predictions
            success_proba = dt.predict_proba(encoded_data)[:, 1]  # Probability of success (class 1)
            
            return success_proba[0]  # Return the predicted success probability
        
        except Exception as e:
            return {'error': str(e)}
        
    def post(self):
        try:
            data = request.json
            result = self.predict_rocket_success(data)
            return jsonify(result)
        except Exception as e:
            return jsonify({'error': str(e)})
        
api.add_resource(RocketSucessAPI, '/predict')
