from flask import session
from flask_restful import Resource
from flask_restful.reqparse import RequestParser

from app.model import *


class LoginAPI(Resource):
    """
        Login Api Resource
    """

    def post(self):
        parser = RequestParser()
        parser.add_argument('login', required=True, help="Login cannot be blank!")
        parser.add_argument('password', required=True, help="Password cannot be blank!")
        args = parser.parse_args()

        if "user" in session and session["user"] is not None:
            return {'AUTH_RESULT': 'ALREADY_LOGGED'}, 201

        userInfo = self.getUserInfoFromCAS(args['login'], args['password'])

        if userInfo is not None:
            user = getUser(login=userInfo['login'])
            if user is not None and isUserAllowed(user["id"]):
                session['user'] = user
                return {'AUTH_RESULT': 'OK'}, 200
            else:
                session['user'] = None
                return {'AUTH_RESULT': 'NOT_ALLOWED'}, 403
        else:
            session['user'] = None
            return {'AUTH_RESULT': 'AUTHENTICATION_FAILED'}, 401

    def delete(self):
        session['user'] = None
        return {'AUTH_RESULT': 'OK'}, 200

    def getUserInfoFromCAS(self, login, password):
        # TODO : A implémenter
        if (login == "admin" or login == "toto") and password == login:
            return {"login": login}
        else:
            return None
