from app.core import api
from app.api.exampleapi import SomeApi

# Some Api resource
api.add_resource(SomeApi, '/api/someapi', '/api/someapi/<int:id>')
