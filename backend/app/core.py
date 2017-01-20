import importlib
from datetime import timedelta

from flask import Flask, session
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.automap import automap_base


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
Base = automap_base()
engine = create_engine(app.config["SQLALCHEMY_DATABASE_URI"])
Base.prepare(engine, reflect=True)

# RestFul Flask
api = Api(app)

# import api resources
importlib.import_module("app.urls")
