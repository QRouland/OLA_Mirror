from flask import session
from flask.ext.restful.reqparse import RequestParser
from flask_restful import Resource

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

        userInfo = self.getUserInfoFromCAS(args['login'], args['password'])

        if userInfo is not None:
            query = USER.select(USER.c.login == userInfo["login"])
            # TODO : check si le user fait partie d'un group actif
            if query.count() == 1:
                session['user'] = query.select().execute().first()
                return {'AUTH_RESULT': 'OK'}, 200
            else:
                return {'AUTH_RESULT': 'NOT_ALLOWED'}, 403
        else:
            return {'AUTH_RESULT': 'AUTHENTICATION_FAILED'}, 401

    def getUserInfoFromCAS(self, login, password):
        pass
