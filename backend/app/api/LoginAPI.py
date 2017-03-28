from hashlib import sha256

from flask import session
from flask_restful import Resource
from flask_restful.reqparse import RequestParser

from app.core import app
from app.model import USER


class LoginAPI(Resource):
    """
        Login Api Resource
    """

    def post(self):
        parser = RequestParser()
        parser.add_argument('email', required=True, help="Email cannot be blank!")
        parser.add_argument('password', required=True, help="Password cannot be blank!")
        args = parser.parse_args()
        email = args['email']
        psw = args['password']
        password = sha256(psw.encode('utf-8')).hexdigest()

        if "user" in session and session["user"] is not None:
            return {'AUTH_RESULT': 'ALREADY_LOGGED'}, 201

        query = USER.select(USER.c.email == email)
        rows = query.execute()
        user = rows.first()

        if app.config['TESTING']:
            if user is not None and psw == email:
                session['user'] = user
                return {'AUTH_RESULT': 'OK'}, 200
            else:
                session['user'] = None
                return {'AUTH_RESULT': 'AUTHENTICATION_FAILED'}, 401
        else:
            if user is not None and password == user.psw:
                session['user'] = user
                return {'AUTH_RESULT': 'OK'}, 200
            else:
                session['user'] = None
                return {'AUTH_RESULT': 'AUTHENTICATION_FAILED'}, 401

    def delete(self):
        session['user'] = None
        return {'AUTH_RESULT': 'OK'}, 200

