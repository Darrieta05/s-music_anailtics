import pprint
from webbrowser import get
from flask import Request, request, session
from flask_restful import Resource
import requests
import json

class User(Resource):
    def get(self):
        f_fill_session = 0 #Flag to let us know if we need to fill the session with user data
        auth_token = False
        if (session.get("id")) :
            auth_token = session.get("auth_token") 
        elif request.headers.get("Postman-Token"):
            f_fill_session = True
            auth_token = request.headers.get("Authorization")
            session["auth_token"] = auth_token
            #TODO: need to get the token expiration date :/ so we can copy it to our redis. also get the refresh token to automate all later....
            # if no refresh token then Panic and user has not authenticated yet.

        res_headers = {"Authorization": auth_token}
        res = requests.get(url="https://api.spotify.com/v1/me", headers=res_headers)
        user_object = json.loads(res.content)

        if f_fill_session :
            if user_object["id"]:
                session["id"] = user_object["id"]
                session["display_name"] = user_object["display_name"]
                session["country"] = user_object["country"]
        return user_object