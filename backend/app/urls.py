from app.core import api

# Some Api resource
api.add_resource(api, '/api/someapi', '/api/someapi/<int:id>')
