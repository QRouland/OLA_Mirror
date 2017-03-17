import os

from flask_restful import Resource, request

from app.core import app
from app.model import *
from app.utils import checkParams


class GroupAPI(Resource):
    """
        Group Api Resource
    """

    def post(self):
        args = request.get_json(cache=False, force=True)
        if not checkParams(['name', 'year', 'class_short', 'class_long', 'department', 'resp_id', 'sec_id'], args):
            return {"ERROR": "One or more parameters are missing !"}, 400

        name = args['name']
        year = args['year']
        class_short = args['class_short']
        class_long = args['class_long']
        department = args['department']
        resp_id = args['resp_id']
        sec_id = args['sec_id']
        res_dir = app.config['BASE_RESSOURCES_DIR'] + name + "/"

        group = getGroup(name=name)
        if group is not None:
            return {"GID": group["id"]}, 200

        user = getUser(uid=resp_id)
        if user is None:
            return {"ERROR": "The user with id " + str(resp_id) + " does not exists !"}, 400
        else:
            if "2" not in user['role'].split('-'):
                role = user['role'] + "-2"
                query = USER.update().values(role=role).where(USER.c.id == resp_id)
                query.execute()

        user = getUser(uid=sec_id)
        if user is None:
            return {"ERROR": "The user with id " + str(sec_id) + " does not exists !"}, 400
        else:
            if "1" not in user['role'].split('-'):
                role = user['role'] + "-1"
                query = USER.update().values(role=role).where(USER.c.id == sec_id)
                query.execute()

        query = GROUP.insert().values(name=name, year=year, class_short=class_short, class_long=class_long,
                                      department=department, resp_id=resp_id, sec_id=sec_id, ressources_dir=res_dir)
        res = query.execute()
        os.mkdir(res_dir)
        return {"GID": res.lastrowid}, 201

    def put(self, gid):
        args = request.get_json(cache=False, force=True)
        if not checkParams(['name', 'year', 'class_short', 'class_long', 'department', 'resp_id', 'sec_id'], args):
            return {"ERROR": "One or more parameters are missing !"}, 400

        name = args['name']
        year = args['year']
        class_short = args['class_short']
        class_long = args['class_long']
        department = args['department']
        resp_id = args['resp_id']
        sec_id = args['sec_id']
        res_dir = app.config['BASE_RESSOURCES_DIR'] + name + "/"

        group = getGroup(gid=gid)
        if group is None:
            return {"ERROR": "This group does not exists !"}, 405

        group2 = getGroup(name=name)
        if group2 is not None:
            return {"ERROR": "A group with this name already exists !"}, 405

        user = getUser(uid=resp_id)
        if user is None:
            return {"ERROR": "The user with id " + str(resp_id) + " does not exists !"}, 400
        else:
            if "2" not in user['role'].split('-'):
                role = user['role'] + "-2"
                query = USER.update().values(role=role).where(USER.c.id == resp_id)
                query.execute()

        user = getUser(uid=sec_id)
        if user is None:
            return {"ERROR": "The user with id " + str(sec_id) + " does not exists !"}, 400
        else:
            if "1" not in user['role'].split('-'):
                role = user['role'] + "-1"
                query = USER.update().values(role=role).where(USER.c.id == sec_id)
                query.execute()

        query = GROUP.update().values(name=name, year=year, class_short=class_short, class_long=class_long,
                                      department=department, resp_id=resp_id, sec_id=sec_id, ressources_dir=res_dir) \
            .where(GROUP.c.id == gid)
        res = query.execute()

        if group["ressources_dir"] != res_dir:
            os.rename(group["ressources_dir"], res_dir)

        return {"GID": gid}, 200

    def get(self, gid=0, name=""):
        if gid > 0:
            return {'GROUP': getGroup(gid=gid)}, 200
        elif name != "":
            return {'GROUP': getGroup(name=name)}, 200
