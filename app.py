import os
import redis
from flask import Flask 
from flask_restful import Api
from flask_session import Session

import redis

from resources.auth import SpotifyAuth
from resources.home import Home
from resources.user import User
from resources.all_playlists import Playlists
from resources.playlist import Playlist
from resources.song import Song
from resources.session_data import Sess

from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

# Configure redis for storing data:
app.secret_key = os.environ.get('SPOTIPY_REDIS_KEY')
app.config['SESSION_TYPE'] = 'redis'
app.config['SESSION_PERMANENT'] = 'False'
app.config['SESSION_USE_SIGNER'] = 'True'
app.config['SESSION_REDIS'] = redis.from_url('redis://127.0.0.1:6379')
api = Api(app)

# Create and initialize the object after app has been configured
session_server = Session(api.app)

api.add_resource(Home, '/')
api.add_resource(SpotifyAuth, '/auth')
api.add_resource(User, '/user')
api.add_resource(Playlists, '/playlists')
api.add_resource(Playlist, '/playlist/<playlist_id>')
api.add_resource(Song, '/song/<id>')
api.add_resource(Sess, '/session')

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)