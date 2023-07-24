import sys
sys.path.append('/Users/dajeong/PycharmProjects/test-automation/')
import os
and_path = os.path.join(os.path.dirname(__file__), '..')
sys.path.append(and_path)

from flask import Flask
from flask_restx import Api
from qa_server.json_control import personal

app = Flask(__name__)
api = Api(app)

# "/personal/{name}" 엔드포인트를 위한 네임스페이스 생성
api.add_namespace(personal.personal_info, '/qa')



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)
