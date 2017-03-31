import os
from datetime import datetime

from dateutil.relativedelta import relativedelta
from flask import session
from flask_restful import Resource, request
from sqlalchemy import and_

from app.api import mailsModels
from app.api.LoginAPI import login_required
from app.model import Roles, getParam, getGroup, getUser, USER, GROUP, TUTORSHIP, LIVRET
from app.utils import send_mail, checkParams


class LivretAPI(Resource):
    """
        Livret Api Resource
    """

    @login_required(roles=[Roles.etudiant])
    def post(self):
        args = request.get_json(cache=False, force=True)
        if not checkParams(['student_id', 'group_id', 'etutor_id', 'company_name', 'company_address', 'contract_type',
                            'contract_start', 'contract_end', 'description'], args):
            return {"ERROR": "One or more parameters are missing !"}, 400

        user = session.get("user")
        group_id = args['group_id']
        etutor_id = args['etutor_id']
        company_name = args['company_name']
        company_address = args['company_address']
        contract_type = int(args['contract_type'])
        contract_start = datetime.strptime(args['contract_start'], "%d-%m-%Y")
        contract_end = datetime.strptime(args['contract_end'], "%d-%m-%Y")
        description = args['description']
        mails = []

        group = getGroup(gid=group_id)
        if group is None:
            return {"ERROR": "This group does not exists !"}, 405

        query = TUTORSHIP.select(and_(TUTORSHIP.c.group_id == group_id, TUTORSHIP.c.student_id == user["id"]))
        res = query.execute()
        tutorship = res.first()

        if tutorship is None:
            return {"ERROR": "This student is not in this group !"}, 405

        tutorship_id = tutorship.id

        user = getUser(uid=etutor_id)
        if user is None:
            return {"ERROR": "The user with id " + str(etutor_id) + " does not exists !"}, 400
        else:
            query = USER.select(USER.c.id == user["id"])
            rows = query.execute()
            res = rows.first()
            if res.hash is not None and len(res.hash) > 0:
                mail = mailsModels.getMailContent("NEW_ETUTOR_ADDED", {"GROUP": group["name"],
                                                                       "URL": getParam('OLA_URL') + "registration/"
                                                                              + res.hash})
            else:
                mail = mailsModels.getMailContent("ETUTOR_ADDED", {"GROUP": group["name"],
                                                                   "URL": getParam('OLA_URL')})

            mails.append((user["email"], mail))
            if str(Roles.tuteur_entreprise) not in user['role'].split('-'):
                return {"ERROR": "The user with id " + str(etutor_id) +
                                 " doesn't have the 'etutor' role (" + str(Roles.tuteur_entreprise) + ") !"}, 400

        if contract_start > contract_end:
            return {"ERROR": "The contract start can't be after its end !"}, 400

        res_dir = group["ressources_dir"] + user['id'] + "/"
        expire = datetime.now() + relativedelta(year=1)

        query = LIVRET.insert().values(tutorship_id=tutorship_id, etutor_id=etutor_id, company_name=company_name,
                                       company_address=company_address, contract_type=contract_type,
                                       contract_start=contract_start, contract_end=contract_end,
                                       description=description, ressources_dir=res_dir, opened='1', expire=expire)
        res = query.execute()
        os.mkdir(res_dir)

        for m in mails:
            addr = m[0]
            mail = m[1]
            send_mail(mail[0], addr, mail[1])

        return {"LID": res.lastrowid}, 201

    @login_required(roles=[Roles.etudiant])
    def put(self, gid):
        args = request.get_json(cache=False, force=True)
        if not checkParams(['name', 'year', 'class_short', 'class_long', 'department', 'resp_id', 'sec_id'], args):
            return {"ERROR": "One or more parameters are missing !"}, 400

        name = args['name'].replace(" ", "_").replace("/", "-")
        year = args['year']
        class_short = args['class_short']
        class_long = args['class_long']
        department = args['department']
        resp_id = args['resp_id']
        sec_id = args['sec_id']
        res_dir = getParam('BASE_DIRECTORY') + name + "/"
        mails = []

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
            query = USER.select(USER.c.id == user["id"])
            rows = query.execute()
            res = rows.first()
            if res.hash is not None and len(res.hash) > 0:
                mail = mailsModels.getMailContent("NEW_RESP_OF_GROUP", {"GROUP": group["name"],
                                                                        "URL": getParam('OLA_URL') + "registration/"
                                                                               + res.hash})
            else:
                mail = mailsModels.getMailContent("RESP_OF_GROUP", {"GROUP": group["name"],
                                                                    "URL": getParam('OLA_URL')})

            mails.append((user["email"], mail))
            if "2" not in user['role'].split('-'):
                role = user['role'] + "-2"
                query = USER.update().values(role=role).where(USER.c.id == resp_id)
                query.execute()

        user = getUser(uid=sec_id)
        if user is None:
            return {"ERROR": "The user with id " + str(sec_id) + " does not exists !"}, 400
        else:
            query = USER.select(USER.c.id == user["id"])
            rows = query.execute()
            res = rows.first()
            if res.hash is not None and len(res.hash) > 0:
                mail = mailsModels.getMailContent("NEW_SEC_OF_GROUP", {"GROUP": group["name"],
                                                                       "URL": getParam('OLA_URL') + "registration/"
                                                                              + res.hash})
            else:
                mail = mailsModels.getMailContent("SEC_OF_GROUP", {"GROUP": group["name"],
                                                                   "URL": getParam('OLA_URL')})

            mails.append((user["email"], mail))
            if "1" not in user['role'].split('-'):
                role = user['role'] + "-1"
                query = USER.update().values(role=role).where(USER.c.id == sec_id)
                query.execute()

        query = GROUP.update().values(name=name, year=year, class_short=class_short, class_long=class_long,
                                      department=department, resp_id=resp_id, sec_id=sec_id, ressources_dir=res_dir) \
            .where(GROUP.c.id == gid)
        query.execute()

        if group["ressources_dir"] != res_dir:
            os.rename(group["ressources_dir"], res_dir)

        for m in mails:
            addr = m[0]
            mail = m[1]
            send_mail(mail[0], addr, mail[1])

        return {"GID": gid}, 200

    @login_required()
    def get(self, gid=0, name=""):
        if gid > 0:
            return {'GROUP': getGroup(gid=gid)}, 200
        elif name != "":
            return {'GROUP': getGroup(name=name)}, 200

    @login_required(roles=Roles.etudiant)
    def options(self, gid):
        args = request.get_json(cache=False, force=True)
        if not checkParams(['pairs'], args):
            return {"ERROR": "One or more parameters are missing !"}, 400

        pairs = args["pairs"]

        group = getGroup(gid=gid)
        if group is None:
            return {"ERROR": "This group does not exists !"}, 405

        for p in pairs:
            try:
                stud = getUser(uid=p[0])
                if stud is None:
                    return {"ERROR": "The user with id " + str(p[0]) + " does not exists !"}, 400
                elif stud['role'] != "4":
                    return {"ERROR": "A student must have the 'student' role !"}, 400

                tutor = getUser(uid=p[1])
                if tutor is None:
                    return {"ERROR": "The user with id " + str(p[1]) + " does not exists !"}, 400
                elif tutor['role'] == "4":
                    return {"ERROR": "A student can't be a tutor !"}, 400
                elif "3" not in tutor['role'].split('-'):
                    role = tutor['role'] + "-3"
                    query = USER.update().values(role=role).where(USER.c.id == p[1])
                    query.execute()
            except IndexError:
                return {"ERROR": "Pairs are incorrectly formed !"}, 409

            query = TUTORSHIP.insert().values(group_id=gid, student_id=p[0], ptutor_id=p[1])
            query.execute()

            query = USER.select(USER.c.id == stud["id"])
            rows = query.execute()
            res = rows.first()
            if res.hash is not None and len(res.hash) > 0:
                mail = mailsModels.getMailContent("NEW_STUD_OF_GROUP", {"GROUP": group["name"],
                                                                        "URL": getParam('OLA_URL') + "registration/"
                                                                               + res.hash})
            else:
                mail = mailsModels.getMailContent("STUD_OF_GROUP", {"GROUP": group["name"],
                                                                    "URL": getParam('OLA_URL')})

            send_mail(mail[0], stud["email"], mail[1])

        return {"RESULT": "Pairs added successfully"}, 200
