import base64
import json
import logging
import os
from flask import redirect, session 
import requests

client_id = os.environ.get('SPOTIPY_CLIENT_ID')
client_secret = os.environ.get('SPOTIPY_CLIENT_SECRET')
redirect_uri = os.environ.get('SPOTIPY_REDIRECT_URI')

# define constants
sp_access_token = "sp_access_token" # Session key for access token

class AuthClientError(RuntimeError):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

def Get_token():
    """checks if the username has a valid token or returns a valid token"""
    if session.get(sp_access_token):
        return session.get(sp_access_token)

def refresh_token():
    url = "https://accounts.spotify.com/api/token"
    req_body_dict = {
        "grant_type": "refresh_token",
        "refresh_token": session["sp_refresh_token"]
    }
    req_header_dict = {"Content-Type": "application/x-www-form-urlencoded",
        "Authorization": "Basic " + build_token()}
    res = requests.post(url=url, data=req_body_dict, headers=req_header_dict)
    res_dict = json.loads(res.content)
    session["sp_access_token"] = res_dict["access_token"]

def renew_access_token(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except AuthClientError:
            # let's renew the token
            refresh_token()
            return func(*args, **kwargs)
    return wrapper
            

def validate_session(func):
    def wrapper(*args, **kwargs):
        token = session.get(sp_access_token)
        if token:
            return func(*args, **kwargs)
        else:
            return redirect("/auth")
    return wrapper


def build_token():
    # check os variables
    if client_id == None or client_secret == None:
        logging.error("Variable CLIENT_ID or CLIENT_SECRET has not been set")

    auth_str = "{}:{}".format(client_id, client_secret)
    b64_auth_str_bytes = base64.b64encode(auth_str.encode('ascii'))
    b64_auth_str = b64_auth_str_bytes.decode('ascii')
    return b64_auth_str