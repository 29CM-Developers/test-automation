import json

from flask import request
from flask_restx import Resource, Namespace

json_list = Namespace('get_lists')
json_path = '/Users/mpark-macmini/test-automation/qa_server/json_control/personal.json'
# "/personal/{name}" 엔드포인트
@json_list.route("/lists")
class JsonLists(Resource):
    def get(self, name):
        try:
            with open(json_path, 'r') as file:
                data = json.load(file)
            return list(data.keys())
        except FileNotFoundError:
            return {'error': 'Data not found'}, 404