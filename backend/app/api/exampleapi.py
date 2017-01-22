from flask_restful import Resource


class SomeApi(Resource):
    """
        Some Api Resource
    """
    def post(self):
        return {'somepost': 'somepostdata'}, 201

    def get(self, id=None):
        return {'someget': 'somegetdata'}, 200

    def delete(self, id=None):
        return {'somedelete': 'somedeletedata'}, 204

    def put(self, id=None):
        return {'someput': 'someputdata'}, 201
