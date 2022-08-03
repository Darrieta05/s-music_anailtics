from flask import render_template, redirect, request, session
from flask_session import Session
from flask_restful import Resource

class Home(Resource):
    def get(self):
        if session.get('username') == None:
            print("user {} has an existing session".format(session.get("username")))
            # check if token expired
            return render_template('user_profile.html')
        else:
            print("the user does not have a session ready")
            return redirect('/auth')