import os
import base64
import webbrowser
import requests
import json
from flask import redirect, session
from flask_restful import Resource
from urllib.parse import urlencode
from flask_restful import reqparse


class SpotifyAuth(Resource):
    client_id = os.environ.get('SPOTIPY_CLIENT_ID')
    client_secret = os.environ.get('SPOTIPY_CLIENT_SECRET')
    redirect_uri = os.environ.get('SPOTIPY_REDIRECT_URI')

    callback_parser = reqparse.RequestParser()
    callback_parser.add_argument('code', type=str, location='args', required=False)
    callback_parser.add_argument('error', type=str, location='args', required=False)

    def get(self):
        args = self.callback_parser.parse_args()
        if session.get("sp_token"):
            # check if we need to refresh the token
            print( "Session already there!")
            return session.get('sp_token')
            
        if args["code"]:
            print('Log: user has code now')
            # we have the Authorization code!
            auth_str = self.client_id+':'+self.client_secret
            b64_auth_str_bytes = base64.b64encode(auth_str.encode('ascii'))
            b64_auth_str = b64_auth_str_bytes.decode('ascii')
            req_body_dict = {
                "grant_type": "authorization_code",
                "code": args["code"],
                "redirect_uri": self.redirect_uri
            }
            req_header_dict = {
                "Content-Type": "application/x-www-form-urlencoded",
                "Authorization": "Basic " + b64_auth_str
            }
            # Send a POST request to url to get the access token
            res = requests.post(url='https://accounts.spotify.com/api/token', data=req_body_dict, headers=req_header_dict)
            res_dict = json.loads(res.content)
            session["sp_token"] = res_dict["access_token"]
            session["refresh_token"] = res_dict["refresh_token"]
            # TODO save the access and refresh into a database rather than a session. Also save the time and expiration date.
            # could use Redis... 
            return "Success"

        elif args["error"]:
            # Something happened getting the Auth code :(
            return(args["error"])
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
            total_url = "{}?{}".format('https://accounts.spotify.com/authorize', query_url)
            return webbrowser(total_url)
            