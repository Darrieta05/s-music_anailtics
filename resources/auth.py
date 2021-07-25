import os
import base64
import requests
from flask import redirect
from flask_restful import Resource
from urllib.parse import urlencode
from flask_restful import reqparse


class SpotifyAuth(Resource):
    cache_path = ".spotipyoauthcache"
    client_id = os.environ.get('SPOTIPY_CLIENT_ID')
    client_secret = os.environ.get('SPOTIPY_CLIENT_SECRET')
    redirect_uri = os.environ.get('SPOTIPY_REDIRECT_URI')

    callback_parser = reqparse.RequestParser()
    callback_parser.add_argument('code', type=str, location='args', required=False)
    callback_parser.add_argument('error', type=str, location='args', required=False)

    def get(self):
        args = self.callback_parser.parse_args()
        if args["code"]:
            # we have the Authorization code!
            post_auth_spotify_token_url = 'https://accounts.spotify.com/api/token'
            body_dict = {
                "grant_type": "authorization_code",
                "code": args["code"],
                "redirect_uri": self.redirect_uri
            },
            header_dict = {
                # Base 64 encoded client_id:client_secret
                "Authorization": base64.encode(self.client_id+':'+self.client_secret)
            }
            # Send a POST request to url to get the access token
            res = requests.post(url=post_auth_spotify_token_url,data=body_dict, headers=header_dict)
            return "Success"
        elif args["error"]:
            # something happened getting the Auth code :(
            return(args["error"])
        else:
            # Lets get the Authorization code from Spotify:
            auth_spotify_url = 'https://accounts.spotify.com/authorize'
            dict_attr = {
                "client_id": self.client_id,
                "response_type": "code",
                "redirect_uri": self.redirect_uri,
                "show_dialog": True,
                "scope": "user-read-private playlist-read-private playlist-modify-private"
            }
            query_url = urlencode(dict_attr)
            total_url = "{}?{}".format(auth_spotify_url, query_url)
            print(total_url)
            return redirect(total_url)
            