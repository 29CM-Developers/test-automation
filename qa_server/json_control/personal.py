import json

from flask import request
from flask_restx import Resource, Namespace

personal_info = Namespace('get_personal')
json_path = '/Users/mpark-macmini/test-automation/qa_server/json_control/personal.json'
# "/personal/{name}" 엔드포인트
@personal_info.route("/personal/<string:name>")
class Personal(Resource):
    def get(self, name):
        try:
            with open(json_path, 'r') as file:
                data = json.load(file)
            return data[f'{name}']
        except FileNotFoundError:
            return {'error': 'Data not found'}, 404

    def post(self, name):
        try:
            json_data = request.get_json()
            insert_key = json_data.get('add_key')
            insert_value = json_data.get('add_value')
            with open(json_path, 'r') as file:
                data = json.load(file)
            data[f'{name}'][f'{insert_key}'] = insert_value
            with open(json_path, 'w') as file:
                try:
                    file.update(data)
                except:
                    pass
                json.dump(data, file)
            return data[f'{name}']
        except FileNotFoundError:
            return {'error': 'Data not found'}, 404

    def delete(self, name):
        try:
            json_data = request.get_json()
            delete_key = json_data.get('delete_key')
            with open(json_path, 'r') as file:
                data = json.load(file)
            del data[f'{name}'][f'{delete_key}']
            with open(json_path, 'w') as file:
                json.dump(data, file)
            return data[f'{name}']
        except FileNotFoundError:
            return {'error': 'Data not found'}, 404
        except KeyError:
            return {'error': '존재하지 않는 key 입니다.'}, 404