from flask_restful import Resource


class Song(Resource):
    def get(self):
        return "Song is:"
