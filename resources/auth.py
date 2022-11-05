import os
import base64
from pprint import pprint
import requests
import json
from flask import redirect, request, session
from flask_restful import Resource
from urllib.parse import urlencode
from flask_restful import reqparse

from common.util import build_token


class SpotifyAuth(Resource):
    redirect_uri = os.environ.get('SPOTIPY_REDIRECT_URI')
    client_id = os.environ.get('SPOTIPY_CLIENT_ID')

    def get(self):
        if "code" in request.args:
            return self.auth_from_spotify()
        elif session.get("sp_access_token"):
            return "Session is open and ready!"
        else:
            print('Log: user will ask for code now, redirecting to spotify page!')
            # Let's get the Auth code from Spotify:
            dict_attr = {
                "client_id": self.client_id,
                "response_type": "code",
                "redirect_uri": self.redirect_uri,
                "show_dialog": True,
                "scope": "user-read-private playlist-read-private playlist-modify-private"
            }
            query_url = urlencode(dict_attr)
            total_url = "{}?{}".format(
                'https://accounts.spotify.com/authorize', query_url)
            return redirect(total_url)

    def auth_from_spotify(self):
        req_body_dict = {
            "grant_type": "authorization_code",
            "code": request.args["code"],
            "redirect_uri": self.redirect_uri
        }
        req_header_dict = {"Content-Type": "application/x-www-form-urlencoded",
            "Authorization": "Basic " + build_token()}
        res = requests.post(url='https://accounts.spotify.com/api/token',
                            data=req_body_dict, headers=req_header_dict)
        res_dict = json.loads(res.content)
        self.session_born(res_dict)
        return "Success" 

    def session_born(self, response_dict):
        session["sp_access_token"] = response_dict["access_token"]
        session["sp_refresh_token"] = response_dict["refresh_token"]
        