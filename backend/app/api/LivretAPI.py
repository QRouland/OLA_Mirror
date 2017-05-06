import os
from datetime import datetime, timedelta

from flask import session
from flask_restful import Resource, request

from app.api import mailsModels
from app.api.LoginAPI import login_required
from app.model import Roles, getParam, getGroup, getUser, USER, LIVRET, getLivret, getTutorship
from app.utils import send_mail, checkParams


class LivretAPI(Resource):
    """
        Livret Api Resource
    """

    @login_required(roles=[Roles.etudiant])
    def post(self):
        args = request.get_json(cache=False, force=True)
        if not checkParams(['group_id', 'etutor_id', 'company_name', 'company_address', 'contract_type',
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

        tutorship = getTutorship(gid=group_id, student=user["id"])

        if tutorship is None:
            return {"ERROR": "This student is not in this group !"}, 405

        tutorship_id = tutorship["id"]

        livret = getLivret(group_id=group_id, student_id=user["id"])
        if livret is not None:
            return {"ERROR": "This livret already exists !"}, 405

        user = getUser(uid=etutor_id)
        if user is None:
            return {"ERROR": "The user with id " + str(etutor_id) + " does not exists !"}, 400
        else:
            query = USER.select(USER.c.id == user["id"])
            rows = query.execute()
            res = rows.first()
            if res.hash is not None and len(res.hash) > 0:
                mail = mailsModels.getMailContent("NEW_ETUTOR_ADDED", {"GROUPE": group["name"],
                                                                       "URL": getParam('OLA_URL') + "registration/"
                                                                              + res.hash})
            else:
                mail = mailsModels.getMailContent("ETUTOR_ADDED", {"GROUPE": group["name"],
                                                                   "URL": getParam('OLA_URL')})

            mails.append((user["email"], mail))
            if str(Roles.tuteur_entreprise) not in user['role'].split('-'):
                return {"ERROR": "The user with id " + str(etutor_id) +
                                 " doesn't have the 'etutor' role (" + str(Roles.tuteur_entreprise) + ") !"}, 400

        if contract_start > contract_end:
            return {"ERROR": "The contract start can't be after its end !"}, 400

        res_dir = group["ressources_dir"] + "/" + str(user['id']) + "/"
        expire = datetime.now() + timedelta(days=365)

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
    def put(self, lid):
        args = request.get_json(cache=False, force=True)
        if not checkParams(['etutor_id', 'company_name', 'company_address', 'contract_type',
                            'contract_start', 'contract_end', 'description'], args):
            return {"ERROR": "One or more parameters are missing !"}, 400

        etutor_id = args['etutor_id']
        company_name = args['company_name']
        company_address = args['company_address']
        contract_type = int(args['contract_type'])
        contract_start = datetime.strptime(args['contract_start'], "%d-%m-%Y")
        contract_end = datetime.strptime(args['contract_end'], "%d-%m-%Y")
        description = args['description']
        mails = []

        livret = getLivret(lid=lid)
        if livret is None:
            return {"ERROR": "This livret does not exists !"}, 405

        user = getUser(uid=etutor_id)
        if user is None:
            return {"ERROR": "The user with id " + str(etutor_id) + " does not exists !"}, 400
        else:
            query = USER.select(USER.c.id == user["id"])
            rows = query.execute()
            res = rows.first()
            if res.hash is not None and len(res.hash) > 0:
                mail = mailsModels.getMailContent("NEW_ETUTOR_ADDED",
                                                  {"GROUPE": livret["tutorship_id"]["group_id"]["name"],
                                                   "URL": getParam('OLA_URL') + "registration/"
                                                          + res.hash})
            else:
                mail = mailsModels.getMailContent("ETUTOR_ADDED", {"GROUPE": livret["tutorship_id"]["group_id"]["name"],
                                                                   "URL": getParam('OLA_URL')})

            mails.append((user["email"], mail))
            if str(Roles.tuteur_entreprise) not in user['role'].split('-'):
                return {"ERROR": "The user with id " + str(etutor_id) +
                                 " doesn't have the 'etutor' role (" + str(Roles.tuteur_entreprise) + ") !"}, 400

        if contract_start > contract_end:
            return {"ERROR": "The contract start can't be after its end !"}, 400

        query = LIVRET.update().values(etutor_id=etutor_id, company_name=company_name,
                                       company_address=company_address, contract_type=contract_type,
                                       contract_start=contract_start, contract_end=contract_end,
                                       description=description) \
            .where(LIVRET.c.id == lid)
        query.execute()

        for m in mails:
            addr = m[0]
            mail = m[1]
            send_mail(mail[0], addr, mail[1])

        return {"LID": lid}, 200

    @login_required()
    def get(self, lid=0, group_id=0, student_id=0):
        if lid > 0:
            return {'LIVRET': getLivret(lid=lid)}, 200
        elif group_id > 0 and student_id > 0:
            return {'LIVRET': getLivret(group_id=group_id, student_id=student_id)}, 200
