from flask_restful import Resource, request

from app.model import *
from app.utils import checkParams


class UserAPI(Resource):
    """
        User Api Resource
    """

    def post(self):
        args = request.get_json(cache=False, force=True)
        if not checkParams(['CASid', 'role'], args):
            return {"ERROR": "One or more parameters are missing !"}, 400

        CASid = args['CASid']
        role = args['role']
        email = self.getEmailFromCAS(CASid)
        phone = None
        user = getUser(login=CASid)
        if user is not None:
            return {"UID": user["id"]}, 200

        if getUser(email=email) is not None:
            return {"ERROR": "A user with this email (" + email + ") already exists !"}, 405

        query = USER.insert().values(login=CASid, email=email, role=role, phone=phone)
        res = query.execute()
        return {"UID": res.lastrowid}, 201

    def put(self, uid):
        args = request.get_json(cache=False, force=True)
        if not checkParams(['CASid', 'role', 'email', 'phone'], args):
            return {"ERROR": "One or more parameters are missing !"}, 400

        CASid = args['CASid']
        role = args['role']
        email = args['email']
        phone = args['phone']

        if getUser(uid=uid) is None:
            return {"ERROR": "This user doesn't exists !"}, 405

        if getUser(login=CASid) is not None:
            return {"ERROR": "A user with this CASid (login) already exists !"}, 405

        if getUser(email=email) is not None:
            return {"ERROR": "A user with this email already exists !"}, 405

        query = USER.update().values(login=CASid, email=email, role=role, phone=phone).where(USER.c.id == uid)
        query.execute()
        return {"UID": uid}, 200

    def get(self, uid=0, login="", email=""):
        if uid > 0:
            return {'USER': getUser(uid=uid)}, 200
        elif login != "":
            return {'USER': getUser(login=login)}, 200
        elif email != "":
            return {'USER': getUser(email=email)}, 200

    @staticmethod
    def getEmailFromCAS(CASid):
        return CASid + "@ola.com"
