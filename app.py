import os
from flask import Flask, request
from flask_restful import Resource, Api

from resources.auth import SpotifyAuth
from resources.home import Home
from resources.callback import Auth_Callback

from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
api = Api(app)

api.add_resource(Home, '/')
api.add_resource(SpotifyAuth, '/auth')
api.add_resource(Auth_Callback, '/auth/callback')

if __name__ == '__main__':
    app.run(debug=True, port=5000)