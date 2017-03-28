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


def getTutorshipForStudent(gid, student):
    query = TUTORSHIP.select(and_(TUTORSHIP.c.group_id == gid, TUTORSHIP.c.student_id == student))
    rows = query.execute()
    res = rows.first()
    if res is not None:
        return {"id": res.id, "group_id": getGroup(gid=res.group_id), "student_id": getUser(uid=res.student_id),
                "ptutor_id": getUser(uid=res.ptutor_id)}
    else:
        return None


def hashExists(test):
    query = USER.select(USER.c.hash == test)
    rows = query.execute()
    res = rows.first()
    return res is not None
