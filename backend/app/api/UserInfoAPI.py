from flask import session
from flask_restful import Resource

from app.model import LIVRET, TUTORSHIP, and_


class UserInfoAPI(Resource):
    """
        UserInfo Api Resource
    """

    def get(self):
        user = session.get("user", None)
        return {'USER': user}, 200


class UserGroupsAPI(Resource):
    """
        UserGroups Api Resource
    """
    def get(self):
        user = session.get("user", None)
        if user is not None:
            subquery = LIVRET.select().distinct().with_only_columns([LIVRET.c.tutorship_id])
            query = TUTORSHIP.select(
                and_(TUTORSHIP.c.student_id == user["id"], TUTORSHIP.c.id.notin_(subquery))).distinct()
            res = query.execute()
            liste = []
            for r in res:
                liste.append(r.group_id)

            return {'GROUP_LIST': liste}, 200
