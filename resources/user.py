from flask import session
from flask_restful import Resource
import requests
import json

class User(Resource):
    def get(self):
        # using the token let's get all the info possible from the user and display it
        print(session.get("sp_token", "not set")) 
        ses_token = session.get("sp_token", "not set yet!!")
        # use the token to make a request.. get all the info from the user.. 
        # let's get the personal info first:
        res_headers = {"Authorization": "Bearer {}".format(ses_token)}
        res = requests.get(url="https://api.spotify.com/v1/me", headers=res_headers)
        return json.loads(res.content)