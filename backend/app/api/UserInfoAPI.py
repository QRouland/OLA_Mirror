from flask import session
from flask_restful import Resource


class UserInfoAPI(Resource):
    """
        UserInfo Api Resource
    """

    def get(self):
        user = session["user"]
        return {'USER': user}, 200
