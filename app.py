import os
from flask import Flask, request
from flask_restful import Resource, Api
from resources.auth import SpotifyAuth
from resources.home import Home


app = Flask(__name__)
api = Api(app)

api.add_resource(Home, '/')
api.add_resource(SpotifyAuth, '/auth')

if __name__ == '__main__':
    app.run(debug=True)