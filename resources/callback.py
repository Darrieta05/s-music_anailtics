from flask_restful import Resource, request

class Auth_Callback(Resource):
    def get(self):
        print(request.args)