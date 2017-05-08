from flask import session
from flask_restful import Resource

from app.api.LoginAPI import login_required
from app.model import getLivret, PERIOD, getPeriod


class GetAllAPI(Resource):
    """
        GetAll Api Resource
        Renvoie toutes les occurences correspondant à un critère
    """

    @login_required()
    def get(self, what, value):
        user = session.get("user")
        result = []

        if what == "periodsOfLivret":  # Toutes les périodes associées à un livret
            if value > 0:
                livret = getLivret(lid=value)
                if livret is None:
                    return {"ERROR": "This livret doesn't exists !"}, 405
                query = PERIOD.select(PERIOD.c.livret_id == value)
                res = query.execute()
                for row in res:
                    result.append(getPeriod(pid=row.id))
        else:
            return {'ERROR': 'Unkown parameter :' + str(what)}, 200

        return {'RESULT': result}, 200
