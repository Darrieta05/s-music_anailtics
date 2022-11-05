from webbrowser import get
from flask import redirect, request, session
from flask_restful import Resource
import requests
import json

from common.util import AuthClientError, renew_access_token, validate_session, sp_access_token

class User(Resource):
    @validate_session
    def get(self):
        return self.user_info()

    @renew_access_token
    def user_info(self):
        url =  "https://api.spotify.com/v1/me"
        res_headers = {"Authorization": "Bearer " + session[sp_access_token]}
        res = requests.get(url="https://api.spotify.com/v1/me", headers=res_headers)
        user_object = json.loads(res.content)
        if res.status_code == 401:
            raise AuthClientError()

        session["id"] = user_object["id"]
        session["display_name"] = user_object["display_name"]
        session["country"] = user_object["country"]
        return user_object

