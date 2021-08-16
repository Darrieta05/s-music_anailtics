from flask_restful import Resource
from flask import session

class Playlists(Resource):
    def get(self):
        ses_token = session.get('sp_token', 'not set')
        # make request to get all playlists
