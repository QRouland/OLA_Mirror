import importlib
from datetime import timedelta

from app.config import Config
from flask import Flask, session
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy import create_engine
from sqlalchemy.ext.automap import automap_base

# initialization Flask
app = Flask(__name__)
app.config.from_object(Config.ACTIVE_CONFIG)

app.permanent_session_lifetime = \
    timedelta(
        minutes=app.config['SESSION_VALIDITY_DURATION_WITHOUT_ACTIVITY_MIN']
    )

@app.before_request
def before_request():
    session.modified = True

# SQLAlchemy
db = SQLAlchemy(app)
Base = automap_base()
engine = create_engine(app.config["SQLALCHEMY_DATABASE_URI"])
Base.prepare(engine, reflect=True)
meta = MetaData(engine, True)

# RestFul Flask
api = Api(app)

# import api resources
importlib.import_module("app.urls")
