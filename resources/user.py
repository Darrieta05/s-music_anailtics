import pprint
from flask import Request, request, session
from flask_restful import Resource
import requests
import json

class User(Resource):
    def get(self):
        # TODO: get access token from request headers
        # right now it works because we are using Postman as a client.

        # if client detected is PostMan, get the AuthToken and save it in a session
        # if is not detected, ask for access token in the session
        # if no access token in the session, go get an access token using the refresh token.
        # if no refresh token then Panic and user has not authenticated yet.


        res_headers = {"Authorization": request.headers.get("Authorization")}
        res = requests.get(url="https://api.spotify.com/v1/me", headers=res_headers)

        # if content.len => save the user email and name in the session to identify later. 
        # Also save the access token
        return json.loads(res.content)