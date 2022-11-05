import json
from flask_restful import Resource
from flask import request, session
import requests

from common.util import AuthClientError, renew_access_token, validate_session, sp_access_token

class Playlists(Resource):
    def build_playlist_url(self):
        format_url = "https://api.spotify.com/v1/me/playlists"
        return format_url

    @validate_session
    def get(self):
        return self.get_playlists()

    @renew_access_token
    def get_playlists(self):
        res_headers = {"Authorization": "Bearer " + session[sp_access_token]}
        url = self.build_playlist_url()
        res = requests.get(url=url, headers=res_headers)
        playlist_object = json.loads(res.content)
        if res.status_code == 401:
            raise AuthClientError()

        for i in playlist_object["items"]:
            print("Found \t{} \twith {} tracks".format(i["name"], i["tracks"]["total"]))

        return playlist_object
    
    def get_playlist_by_id(self, id):
        res_headers = {"Authorization": "Bearer " + session[sp_access_token]}