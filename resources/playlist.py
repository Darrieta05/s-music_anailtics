import json
from flask_restful import Resource
from flask import request, session
import requests

class Playlist(Resource):
    def build_playlist_url(self, user_id):
        format_url = str("https://api.spotify.com/v1/users/{}/playlists").format(user_id)
        return format_url

    def get(self):
        f_fill_session = 0 #Flag to let us know if we need to fill the session with user data
        auth_token = False
        if (session.get("id")) :
            auth_token = session.get("auth_token") 
        elif request.headers.get("Postman-Token"):
            f_fill_session = True
            auth_token = request.headers.get("Authorization")
            session["auth_token"] = auth_token

        res_headers = {"Authorization": auth_token}
        playlist_url = self.build_playlist_url(session["id"])
        res = requests.get(url=playlist_url, headers=res_headers)
        playlist_object = json.loads(res.content)

        #return all playlists names:
        for i in playlist_object["items"]:
            print("Found \t{} \twith {} tracks".format(i["name"], i["tracks"]["total"]))

        return playlist_object