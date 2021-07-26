from flask import session
from flask_restful import Resource

class User(Resource):
    def get(self):
        # using the token let's get all the info possible from the user and display it
        print(session.get("sp_token")) 
        return