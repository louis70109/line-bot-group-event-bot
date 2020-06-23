from flask import Flask
from flask_restful import Api

from controller.line_controller import LineGroupController

app = Flask(__name__)

api = Api(app)
api.add_resource(LineGroupController, '/webhooks/line')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
