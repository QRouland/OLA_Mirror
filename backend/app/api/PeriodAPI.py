import os
from datetime import datetime

from flask import session
from flask_restful import Resource, request
from sqlalchemy import select, and_

from app.api import mailsModels
from app.api.LoginAPI import login_required
from app.model import Roles, getParam, getGroup, getUser, LIVRET, getLivret, TUTORSHIP, PERIOD, getPeriod, \
    TypesPeriode
from app.utils import send_mail, checkParams, get_random_string


class PeriodAPI(Resource):
    """
        Period Api Resource
    """

    @login_required(roles=[Roles.resp_formation])
    def post(self):
        args = request.get_json(cache=False, force=True)
        if not checkParams(['group_id', 'period_type', 'start', 'end'], args):
            return {"ERROR": "One or more parameters are missing !"}, 400

        group_id = args['group_id']
        period_type = args['period_type']
        start = datetime.strptime(args['start'], "%d-%m-%Y")
        end = datetime.strptime(args['end'], "%d-%m-%Y")

        # On vérifie que le groupe existe
        group = getGroup(gid=group_id)
        if group is None:
            return {"ERROR": "This group with id " + str(group_id) + "does not exists !"}, 405

        if start > end:
            return {"ERROR": "The period's start can't be after its end !"}, 400

        # On vérifie que l'utilisateur actuel a le droit de modifier ce groupe
        user = session.get("user")
        if user["id"] != group["resp_id"]:
            return {"ERROR": "UNAUTHORIZED"}, 401

        # On récupère tous les livrets de ce groupe
        query = select([LIVRET.c.id, TUTORSHIP.c.student_id]).where(
            and_(TUTORSHIP.c.id == LIVRET.c.tutorship_id, TUTORSHIP.c.group_id == group_id))
        res = query.execute()

        # Pour chaque livret du groupe on ajoute la période et on prévient l'étudiant
        for row in res:
            # On crée un répertoire avec un nom aléatoire
            res_dir = group["ressources_dir"] + "/" + str(row.student_id) + "/" + get_random_string() + "/"
            while os.path.exists(res_dir):
                res_dir = group["ressources_dir"] + "/" + str(row.student_id) + "/" + get_random_string() + "/"

            # Enregistrement des infos en base
            query = PERIOD.insert().values(livret_id=row.id, type=period_type, start=start, end=end,
                                           ressources_dir=res_dir)
            query.execute()
            os.mkdir(res_dir)

            # Envoi d'un mail
            mail = mailsModels.getMailContent("NEW_PERIOD", {"GROUPE": group["name"],
                                                             "URL": getParam('OLA_URL') + "mon_livret"})
            send_mail(mail[0], getUser(row.student_id)["email"], mail[1])

        return {"RESULT": "OK"}, 201

    @login_required(roles=[Roles.etudiant, Roles.tuteur_entreprise])
    def put(self, pid):
        args = request.get_json(cache=False, force=True)
        if not checkParams(['text'], args):
            return {"ERROR": "One or more parameters are missing !"}, 400

        text = args['text']
        user = session.get("user")
        mails = []

        # On vérifie que la période existe
        period = getPeriod(pid)
        if period is None:
            return {"ERROR": "This period does not exists !"}, 405

        # On vérifie que l'utilisateur actuel a le droit de modifier ce livret (étudiant ou tuteur)
        livret = getLivret(lid=period["livret_id"])
        if user["id"] != livret["etutor_id"]["id"] and user["id"] != livret["tutorship_id"]["student_id"]["id"]:
            return {"ERROR": "UNAUTHORIZED"}, 401

        # Si c'est le commentaire de l'étudiant, on prévient le tuteur
        if user["role"] == str(Roles.etudiant):
            mail = mailsModels.getMailContent("STUD_COMMENT_ADDED", {"ETUDIANT": user["name"],
                                                                     "URL": getParam('OLA_URL')})
            mails.append((user["email"], mail))
            query = PERIOD.update().values(student_desc=text).where(PERIOD.c.id == pid)
        else:  # Sinon on vérifie que c'est une période d'entreprise
            if period["type"] == TypesPeriode.universitaire:
                return {"ERROR": "A tutor can't modify a university period !"}, 405

            mail = mailsModels.getMailContent("ETUTOR_COMMENT_ADDED", {"TUTEUR": user["name"],
                                                                       "URL": getParam('OLA_URL')})
            mails.append((user["email"], mail))
            query = PERIOD.update().values(etutor_desc=text).where(PERIOD.c.id == pid)

        query.execute()

        for m in mails:
            addr = m[0]
            mail = m[1]
            send_mail(mail[0], addr, mail[1])

        return {"PID": pid}, 200

    @login_required()
    def get(self, pid):
        if pid > 0:
            return {'PERIOD': getPeriod(pid=pid)}, 200
