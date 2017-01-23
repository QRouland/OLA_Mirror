from app.api.exampleapi import SomeApi
from app.api.loginAPI import LoginAPI
from app.core import api

# Some Api resource
api.add_resource(SomeApi, '/api/someapi', '/api/someapi/<int:id>')
api.add_resource(LoginAPI, '/api/login', '/api/login')
