import os
import requests
from flask_restful import Resource
import spotipy
from spotipy import oauth2
from dotenv import load_dotenv

load_dotenv()

PORT_NUMBER = 8080
client_id = os.environ.get('SPOTIPY_CLIENT_ID')
client_secret = os.environ.get('SPOTIPY_CLIENT_SECRET')
redirect_uri = os.environ.get('SPOTIPY_REDIRECT_URI')


scope = "playlist-read-private"
cache_path = ".spotipyoauthcache"

sp_oauth = oauth2.SpotifyOAuth( client_id, client_secret, redirect_uri, scope=scope, cache_path=cache_path)


class SpotifyAuth(Resource):
    def get(self):
        pass
    