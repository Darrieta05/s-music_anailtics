import flask
from flask_restful import Resource

class Home(Resource):
    def get(self):
        return flask.make_response("<a href='http://localhost:5000/auth'>Login to spotify</a>")