import json
from flask_restful import Resource
from flask import request, session
import requests

from common.util import AuthClientError, renew_access_token, validate_session

class Playlist(Resource):
    def build_playlist_url(self, user_id):
        format_url = str("https://api.spotify.com/v1/users/{}/playlists").format(user_id)
        return format_url

    @validate_session
    def get(self):
        return self.get_playlists(session["sp_access_token"])

    @renew_access_token
    def get_playlists(self, access_token):
        res_headers = {"Authorization": "Bearer " + access_token}
        url = self.build_playlist_url(session["id"])
        res = requests.get(url=url, headers=res_headers)
        playlist_object = json.loads(res.content)
        if res.status_code == 401:
            raise AuthClientError()

        for i in playlist_object["items"]:
            print("Found \t{} \twith {} tracks".format(i["name"], i["tracks"]["total"]))

        return playlist_object