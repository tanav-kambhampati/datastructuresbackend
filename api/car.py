from flask import Blueprint, jsonify, request
from flask_restful import Api, Resource, reqparse
from __init__ import db
from model.cars import Car  # Import the car model
import requests

# Create a Blueprint for the car API
car_api = Blueprint('car_api', __name__, url_prefix='/api/car')

# Create the API instance
api = Api(car_api)

class CarAPI:
    class _Create(Resource):
        def post(self):
            # Get request JSON data
            body = request.get_json()

            # Extract car information
            make = body.get('make')
            model = body.get('model')
            year = body.get('year')
            fuel = body.get('fuel')
            cylinders = body.get('cylinders')

            # Create a new car object
            car_obj = Car(make=make, model=model, year=year, fuel=fuel, cylinders=cylinders)

#2: Key Code block to add car to database 
            # create car in database
            car = car_obj.create()
            # success returns json of car
            if car:
                return jsonify(car.read())
            # failure returns error
            return {'message': f'Invalid input, correct fields should be make, model, year, and fuel, cylinders'}, 400

            
    class _Read(Resource):
        def get(self):
        # Retrieve all cars from the database
            Cars = Car.query.all()
            json_ready = [car.to_dict() for car in Cars]
        # Return the JSON response
            return jsonify(json_ready)

    # building RESTapi resources/interfaces, these routes are added to Web Server
    api.add_resource(_Create, '/create')
    api.add_resource(_Read, '/')