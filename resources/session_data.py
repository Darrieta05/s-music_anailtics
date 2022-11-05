from flask import session
from flask_restful import Resource

class Sess(Resource):
    def get(self):
        # print out all the session data available
        print(session.get("sp_token", "no token saved"))
        json_to_see = {
            "sp_access_token": session.get("sp_access_token"),
            "session_token": session.get("sp_token"),
            "user_id": session.get("user_id"),
        }
        return json_to_see