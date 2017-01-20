import os


class Config:
    DEBUG = False
    TESTING = False
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = \
        'sqlite:///' + os.path.join(BASE_DIR, '../app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    THREADS_PER_PAGE = 2
    SECRET_KEY = "secret"
    BUNDLE_ERRORS = True
    SESSION_COOKIE_SECURE = True
    SESSION_VALIDITY_DURATION_WITHOUT_ACTIVITY_MIN = 20


class Prod(Config):
    SQLALCHEMY_DATABASE_URI = 'mysql://user@localhost/foo'


class Debug(Config):
    DEBUG = True
    SESSION_COOKIE_SECURE = False
    SQLALCHEMY_DATABASE_URI = 'mysql://ola:ola@localhost/OLA'


class Test(Config):
    TESTING = True
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = \
        'sqlite:///' + os.path.join(BASE_DIR, '../test.db')
