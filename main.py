# initial file to get the info from spotify api

# set up the connection to spotipy
from dotenv import load_dotenv
import os
import json
import spotipy
import pandas as pd
from spotipy import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth

load_dotenv()

client_id = os.environ.get('SPOTIPY_CLIENT_ID')
client_secret = os.environ.get('SPOTIPY_CLIENT_SECRET')

client_credentials_manager = SpotifyClientCredentials(client_id, client_secret)
#sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

scope = "playlist-read-private"
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))



playlists = sp.current_user_playlists(limit=50)
while playlists:
    for i, playlist in enumerate(playlists['items']):
        print("{} {} {}".format( playlist['uri'], playlist['name']))
    if playlists['next']:
        playlists = sp.next(playlists)
    else:
        playlists = None


print("\n \n \n \n")




playlist_id = 'spotify:playlist:6KR7tSia1fLNqLqotrSIJT'
results = sp.playlist(playlist_id)

print(*results.keys())

print(type(results.get("tracks").get("items")))

for x in results.get("tracks").get('items'):
    track = x["track"]
    print(track["name"])

def main():
    print("-------it works!") 

main()