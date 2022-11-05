from flask import render_template, redirect, request, session
from flask_session import Session
from flask_restful import Resource

from common.util import validate_session

class Home(Resource):
    @validate_session
    def get(self):
       return "Welcome ;)" 