from hashlib import sha256

from flask_restful import Resource, request

from app.model import *
from app.utils import checkParams, get_random_string


class UserAPI(Resource):
    """
        User Api Resource
    """

    def post(self):
        args = request.get_json(cache=False, force=True)
        if not checkParams(['role', 'email', 'name'], args):
            return {"ERROR": "One or more parameters are missing !"}, 400

        role = args['role']
        email = args['email']
        name = args['name']
        phone = None
        user = getUser(email=email)
        hashpass = get_random_string()
        while hashExists(hashpass):
            hashpass = get_random_string()

        if user is not None:
            return {"UID": user["id"]}, 200

        query = USER.insert().values(email=email, role=role, phone=phone, name=name, hash=hashpass)
        res = query.execute()
        return {"UID": res.lastrowid}, 201

    def put(self, uid):
        args = request.get_json(cache=False, force=True)
        if not checkParams(['role', 'email', 'phone', 'name', 'password'], args):
            return {"ERROR": "One or more parameters are missing !"}, 400

        role = args['role']
        email = args['email']
        phone = args['phone']
        name = args['name']
        psw = args['password']

        if psw is None or len(psw) < 8:
            return {"ERROR": "Password can't be empty or less than 8 characters !"}, 400

        password = sha256(psw).hexdigest()

        if getUser(uid=uid) is None:
            return {"ERROR": "This user doesn't exists !"}, 405

        if getUser(email=email) is not None:
            return {"ERROR": "A user with this email already exists !"}, 405

        query = USER.update().values(email=email, role=role, phone=phone, name=name, psw=password, hash=None) \
            .where(USER.c.id == uid)
        query.execute()
        return {"UID": uid}, 200

    def get(self, uid=0, email=""):
        if uid > 0:
            return {'USER': getUser(uid=uid)}, 200
        elif email != "":
            return {'USER': getUser(email=email)}, 200
