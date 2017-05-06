from sqlalchemy import Table
from sqlalchemy import and_

from app.core import meta, Base

USER = Table('USER', meta, autoload=False)
SETTINGS = Table('SETTINGS', meta, autoload=False)
GROUP = Table('GROUP', meta, autoload=False)
TUTORSHIP = Table('TUTORSHIP', meta, autoload=False)
PERIOD = Table('PERIOD', meta, autoload=False)
LIVRET = Table('LIVRET', meta, autoload=False)

user_class = Base.classes.USER
settings_class = Base.classes.SETTINGS
group_class = Base.classes.GROUP
tutorship_class = Base.classes.TUTORSHIP
period_class = Base.classes.PERIOD
livret_class = Base.classes.LIVRET


def getParam(key):
    query = SETTINGS.select(SETTINGS.c.key == key)
    rows = query.execute()
    return rows.first().value


def getUser(uid=0, email="", hashcode=""):
    res = None

    if uid == 0 and email == "" and hashcode == "":
        raise Exception("getUser must be called with one argument !")
    else:
        if uid != 0:
            query = USER.select(USER.c.id == uid)
            rows = query.execute()
            res = rows.first()

        elif email != "":
            query = USER.select(USER.c.email == email)
            rows = query.execute()
            res = rows.first()

        elif hashcode != "":
            query = USER.select(USER.c.hash == hashcode)
            rows = query.execute()
            res = rows.first()

        if res is not None:
            return {"id": res.id, "email": res.email, "role": res.role, "phone": res.phone, "name": res.name}
        else:
            return None


def getGroup(gid=0, name=""):
    res = None

    if gid == 0 and name == "":
        raise Exception("getGroup must be called with one argument !")
    else:
        if gid != 0:
            query = GROUP.select(GROUP.c.id == gid)
            rows = query.execute()
            res = rows.first()

        elif name != "":
            query = GROUP.select(GROUP.c.name == name)
            rows = query.execute()
            res = rows.first()

        if res is not None:
            return {"id": res.id, "name": res.name, "year": res.year, "class_short": res.class_short,
                    "class_long": res.class_long, "department": res.department, "resp_id": getUser(uid=res.resp_id),
                    "sec_id": getUser(uid=res.sec_id), "ressources_dir": res.ressources_dir}
        else:
            return None


def getTutorship(tid=0, gid=0, student=0):
    if tid == 0 and gid == 0 and student == 0:
        raise Exception("getGroup must be called with at least one argument !")
    else:
        if gid != 0:
            query = TUTORSHIP.select(and_(TUTORSHIP.c.group_id == gid, TUTORSHIP.c.student_id == student))
            rows = query.execute()
            res = rows.first()
        elif tid != 0:
            query = TUTORSHIP.select(TUTORSHIP.c.id == tid)
            rows = query.execute()
            res = rows.first()
        else:
            raise Exception("getTutorship must be called with two parameter for group+student search !")

        if res is not None:
            return {"id": res.id, "group_id": getGroup(gid=res.group_id), "student_id": getUser(uid=res.student_id),
                    "ptutor_id": getUser(uid=res.ptutor_id)}
        else:
            return None


def getLivret(lid=0, group_id=0, student_id=0):
    res = None

    if lid == 0 and student_id == "":
        raise Exception("getLivret must be called with at least one argument !")
    else:
        if lid != 0:
            query = LIVRET.select(LIVRET.c.id == lid)
            rows = query.execute()
            res = rows.first()

        elif student_id != 0 and group_id != 0:
            tutorship = getTutorship(gid=group_id, student=student_id)
            if tutorship is None:
                return None
            query = LIVRET.select(LIVRET.c.tutorship_id == tutorship["id"])
            rows = query.execute()
            res = rows.first()
        else:
            raise Exception("getLivret must be called with two parameter for group+student search !")

        if res is not None:
            return {"id": res.id, "tutorship_id": getTutorship(tid=res.tutorship_id),
                    "etutor_id": getUser(uid=res.etutor_id), "company_name": res.company_name,
                    "company_address": res.company_address, "contract_type": res.contract_type,
                    "contract_start": res.contract_start.strftime('%d-%m-%Y'),
                    "contract_end": res.contract_end.strftime('%d-%m-%Y'),
                    "ressources_dir": res.ressources_dir, "opened": res.opened,
                    "expire": res.expire.strftime('%d-%m-%Y')}
        else:
            return None


def hashExists(test):
    query = USER.select(USER.c.hash == test)
    rows = query.execute()
    res = rows.first()
    return res is not None


class Roles:
    secretaire = 1
    resp_formation = 2
    tuteur_univ = 3
    etudiant = 4
    tuteur_entreprise = 5
