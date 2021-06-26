import os
from flask import Flask, request
from flask_restful import Resource, Api
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

app = Flask(__name__)

@app.route('/')
def index():
    access_token = ""    
    token_info = sp_oauth.get_cached_token()

    if token_info:
        print("Found cached token!")
        access_token = token_info['access_token']
    else: 
        url = request.url
        code = sp_oauth.parse_response_code(url)
        if code != url:
            print("Found spotify auth code in Request URL! Trying to get valid access token...")
            token_info = oauth2.get_access_token(code)
            access_token = token_info['access_token']
    
    if access_token:
        print("Access token available! Trying to get user information...")
        sp = spotipy.Spotify(access_token)
        results = sp.current_user()
        return results
    else:
        return htmlforLoginButton()

def htmlforLoginButton():
    auth_url = getSPOauthURI()
    htmlLoginButton = "<a href='" + auth_url + "'>Login to Spotify</a>"
    return htmlforLoginButton


def getSPOauthURI():
    auth_url = sp_oauth.get_authorize_url()
    return auth_url


if __name__ == '__main__':
    app.run(debug=True, port=5000)