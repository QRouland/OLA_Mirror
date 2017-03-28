from flask_restful import Resource
from flask_restful.reqparse import RequestParser
from app.tools.LibPdf import delete_file
from model import getParam

import os

class PdfAPI(Resource):
    """
        Pdf Api Resource
    """

    def delete(self):
        parser = RequestParser()
        parser.add_argument('templateName', required=True, help="Template name is required !")
        args = parser.parse_args()

        if ".." in args:
            return { "msg" : ".. not allowed in path"}, 400

        delete_file(os.path.join(getParam('TEMPLATES_DIRECTORY'), args['templateName']))
