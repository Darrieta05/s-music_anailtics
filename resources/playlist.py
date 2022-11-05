import json
from flask_restful import Resource
from flask import request, session
import requests

from common.util import AuthClientError, renew_access_token, validate_session, sp_access_token

class Playlist(Resource):
    def build_playlist_url(self, playlist_id):
        format_url = "https://api.spotify.com/v1/playlists/{}".format(playlist_id)
        return format_url

    @validate_session
    def get(self, playlist_id):
        return self.get_playlist(playlist_id)

    @renew_access_token
    def get_playlist(self, playlist_id):
        res_headers = {"Authorization": "Bearer " + session[sp_access_token]}
        url = self.build_playlist_url(playlist_id)
        res = requests.get(url=url, headers=res_headers)
        playlist_object = json.loads(res.content)
        if res.status_code == 401:
            raise AuthClientError()

        return playlist_object