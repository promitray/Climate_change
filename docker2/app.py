from flask import Blueprint, Flask,jsonify, request
from flask_restful import Api, Resource, reqparse
from flask_restful import Resource
from database import *
import traceback
from datetime import datetime

RESTAPI = Flask(__name__)
API = Api(RESTAPI)

class test(Resource):
    def get(self):
        return {"message": "Hello, World!"}

class Weather(Resource):
    def get(self):
        try:
            data = {}
            print(request.args)
            if 'start_date' in request.args:
                data['start_date'] = request.args['start_date']
            if 'end_date' in request.args:
                data['end_date'] = request.args['end_date']
            else:
                data['end_date'] = str(datetime.now())
            if 'limit_number' in request.args:
                data['limit_number'] = request.args['limit_number']
            else:
               data['limit_number'] = 10 
            print(data)
            if  len(data)<1:
                   return {'message': 'No input data provided'}, 400
            status_code,result = getRecords(data)
            if status_code == 200:
                return { "status": 'success',"result":result }, 201
            else:
                return { "status": 'Internal Error' }, 500
        except Exception as e:
            print(e)
            traceback.print_exc()
        
    def post(self):
        try:
            json_data = request.get_json(force=True)
            print(json_data)
            if not json_data:
                   return {'message': 'No input data provided'}, 400
            status_code = insertRecord(json_data)
            if status_code == 200:
                return { "status": 'success' }, 201
            elif status_code == 401:
                return { "status": 'Record Already Exists' }, 403
            else:
                return { "status": 'Internal Error' }, 500
        except Exception as e:
            print(e)
            traceback.print_exc()

    def put(self):
        try:
            json_data = request.get_json(force=True)
            print(json_data)
            if not json_data:
                   return {'message': 'No input data provided'}, 400
            status_code = updateRecord(json_data)
            if status_code == 200:
                return { "status": 'success' }, 201
            else:
                return { "status": 'Internal Error' }, 500
        except Exception as e:
            print(e)
            traceback.print_exc()

# Route
API.add_resource(Weather, '/Weather')
API.add_resource(test, '/test')
    
if __name__ == '__main__':
    RESTAPI.run(debug=True, host='0.0.0.0',port='5000')
