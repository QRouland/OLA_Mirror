from hashlib import sha256

from flask import session, request
from flask_restful import Resource

from app.core import app
from app.model import USER, getUser
from app.utils import checkParams


class LoginAPI(Resource):
    """
        Login Api Resource
    """

    def post(self):
        args = request.get_json(cache=False, force=True)
        if not checkParams(['email', 'password'], args):
            return {"ERROR": "One or more parameters are missing !"}, 400
        email = args['email']
        psw = args['password']
        password = sha256(psw.encode('utf-8')).hexdigest()

        if "user" in session and session["user"] is not None:
            return {'AUTH_RESULT': 'ALREADY_LOGGED'}, 201

        query = USER.select(USER.c.email == email)
        rows = query.execute()
        res = rows.first()

        if app.config['TESTING']:
            if res is not None and psw == email:
                user = getUser(uid=res.id)
                session['user'] = user
                return {'AUTH_RESULT': 'OK'}, 200
            else:
                session['user'] = None
                return {'AUTH_RESULT': 'AUTHENTICATION_FAILED'}, 401
        else:
            if res is not None and password != "" and password == res.psw:
                user = getUser(uid=res.id)
                session['user'] = user
                return {'AUTH_RESULT': 'OK'}, 200
            else:
                session['user'] = None
                return {'AUTH_RESULT': 'AUTHENTICATION_FAILED'}, 401

    def delete(self):
        session['user'] = None
        return {'AUTH_RESULT': 'OK'}, 200


def login_required(roles=[]):
    def my_login_required(func):
        def wrapper(*args, **kvargs):
            current_user = session.get('user', None)
            if current_user is None or (len(roles) != 0 and not sum([1 for x in current_user['role'].split("-") if int(x) in roles]) > 0):
                return {"ERROR": "UNAUTHORIZED"}, 401
            return func(*args, **kvargs)
        return wrapper
    return my_login_required

