from flask import Flask
from flask_restful import Api
from dotenv import load_dotenv
load_dotenv()

from controller.line_controller import LineGroupController
from controller.echo_controller import EchoController

app = Flask(__name__)

api = Api(app)
api.add_resource(EchoController, '/v1/webhooks/line')
api.add_resource(LineGroupController, '/v2/webhooks/line')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
