import random
import string
from hashlib import sha512

from flask import json
from mailer import Mailer
from mailer import Message
from sqlalchemy.ext.declarative import DeclarativeMeta

from app.core import app

SIMPLE_CHARS = string.ascii_letters + string.digits


def get_random_string(length=32):
    return ''.join(random.choice(SIMPLE_CHARS) for i in range(length))


def get_random_hash(length=64):
    hash = sha512()
    hash.update(get_random_string())
    return hash.hexdigest()[:length]


def new_alchemy_encoder(revisit_self=False, fields_to_expand=[]):
    _visited_objs = []

    class AlchemyEncoder(json.JSONEncoder):
        def default(self, obj):
            if isinstance(obj.__class__, DeclarativeMeta):
                # don't re-visit self
                if revisit_self:
                    if obj in _visited_objs:
                        return None
                    _visited_objs.append(obj)

                # go through each field in this SQLalchemy class
                fields = {}
                for field in [x for x in dir(obj) if not x.startswith('_') and x != 'metadata']:
                    val = obj.__getattribute__(field)

                    # is this field another SQLalchemy object, or a list of SQLalchemy objects?
                    if isinstance(val.__class__, DeclarativeMeta) or (
                                    isinstance(val, list) and len(val) > 0 and isinstance(val[0].__class__,
                                                                                          DeclarativeMeta)):
                        # unless we're expanding this field, stop here
                        if field not in fields_to_expand:
                            # not expanding this field: set it to None and continue
                            fields[field] = None
                            continue

                    fields[field] = val
                # a json-encodable dict
                return fields

            return json.JSONEncoder.default(self, obj)

    return AlchemyEncoder


def checkParams(wanted, args):
    inter = [elt for elt in wanted if elt in args]
    return len(inter) == len(wanted)


def send_mail(subject, to, html):
    if app.config['MAILER']:
        message = Message(From="ola.noreply@univ-tlse2.fr", To=to, charset="utf-8")
        message.Subject = subject
        message.Html = html
        sender = Mailer('localhost')  # TODO: Mettre le SMTP de la fac ici
        sender.send(message)
