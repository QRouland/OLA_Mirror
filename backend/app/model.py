from sqlalchemy import Table
from sqlalchemy import or_

from app.core import meta, db, Base

USER = Table('USER', meta, autoload=False)
SETTINGS = Table('SETTINGS', meta, autoload=False)
HASHTABLE = Table('HASHTABLE', meta, autoload=False)
GROUP = Table('GROUP', meta, autoload=False)
TUTORSHIP = Table('TUTORSHIP', meta, autoload=False)
PERIOD = Table('PERIOD', meta, autoload=False)
LIVRET = Table('LIVRET', meta, autoload=False)

user_class = Base.classes.USER
settings_class = Base.classes.SETTINGS
hashtable_class = Base.classes.HASHTABLE
group_class = Base.classes.GROUP
tutorship_class = Base.classes.TUTORSHIP
period_class = Base.classes.PERIOD
livret_class = Base.classes.LIVRET


def getUser(uid=0, login="", email=""):
    res = None

    if uid == 0 and login == "" and email == "":
        raise Exception("getUser must be called with one argument !")
    else:
        if uid != 0:
            res = db.session.query(user_class).get(uid)

        elif login != "":
            query = USER.select(USER.c.login == login)
            rows = query.execute()
            res = rows.first()

        elif email != "":
            query = USER.select(USER.c.email == email)
            rows = query.execute()
            res = rows.first()

        if res is not None:
            return {"id": res.id, "login": res.login, "email": res.email, "role": res.role, "phone": res.phone}
        else:
            return None


def isUserAllowed(uid):
    query = db.session.query(group_class, tutorship_class).join(tutorship_class) \
        .filter(or_(tutorship_class.student_id == uid, group_class.resp_id == uid))
    res = query.all()
    return res is not None and len(res) > 0
