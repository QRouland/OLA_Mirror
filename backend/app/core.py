from datetime import timedelta

from flask import Flask, session
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy

import importlib


def configure_app(config="prod"):
    if config.lower() == "debug":
        app.config.from_object('app.config.Debug')
    elif config.lower() == "test":
        app.config.from_object('app.config.Test')
    else:
        app.config.from_object('app.config.Prod')

    app.permanent_session_lifetime = \
        timedelta(
            minutes=app.config
            ['SESSION_VALIDITY_DURATION_WITHOUT_ACTIVITY_MIN']
        )

    @app.before_request
    def before_request():
        session.modified = True


# initialization Flask
app = Flask(__name__)
configure_app()

# SQLAlchemy
db = SQLAlchemy(app)

# RestFul Flask
api = Api(app)

# import api resources
importlib.import_module("app.urls")
