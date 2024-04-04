from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource
from model.vehiclesmodel import DecisionTreeClassifier as dt
from model.vehiclesmodel import OneHotEncoder as enc
from sklearn.linear_model import LogisticRegression
import pandas as pd

vechicles_api = Blueprint('vehicles_api', __name__, url_prefix='/api/vehicles')
api = Api(vechicles_api)

# payload_mass,origin_country,company,engine_strength,success_rate

dt = dt  # Assuming dt is already trained
enc = enc  # Assuming enc is already initialized and fitted
class VehiclesAPI(Resource):

    def __init__(self):
        carsalarydata = pd.read_csv('carsalarydata.csv')
        td = carsalarydata.copy()

        self.logreg = LogisticRegression(max_iter=1000)
        X = td.drop('Affordability', axis=1)
        y = td['Affordability']
        self.logreg.fit(X, y)

    def vehicles(Salary):
        try:
            # Preprocess the input data
            data = pd.DataFrame({'Salary': [Salary]})
            encoded_data = enc.transform(data)
            
            # Make predictions
            success_proba = dt.predict_proba(encoded_data)[:, 1]  # Probability of success (class 1)
            
            return success_proba[0]  # Return the predicted success probability
        
        except Exception as e:
            return {'error': str(e)}
        
    def post(self):
        try:
            data = request.json
            result = self.vehicles(data["Salary"])
            return jsonify(result)
        except Exception as e:
            return jsonify({'error': str(e)})
        
api.add_resource(VehiclesAPI, '/predict')
