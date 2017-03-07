import importlib
from datetime import timedelta

from flask_cas import CAS

from app.config import Config
from flask import Flask, session, redirect
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

# Cas Flask
cas = CAS(app)

@app.route('/redirect')
def after_login():
    return redirect("/api/login")

# import api resources
importlib.import_module("app.urls")
