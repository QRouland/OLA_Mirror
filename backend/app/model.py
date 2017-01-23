from app.core import meta
from sqlalchemy import Table

USER = Table('USER', meta, autoload=False)
SETTINGS = Table('SETTINGS', meta, autoload=False)
HASHTABLE = Table('HASHTABLE', meta, autoload=False)
GROUP = Table('GROUP', meta, autoload=False)
TUTORSHIP = Table('TUTORSHIP', meta, autoload=False)
PERIOD = Table('PERIOD', meta, autoload=False)
LIVRET = Table('LIVRET', meta, autoload=False)
