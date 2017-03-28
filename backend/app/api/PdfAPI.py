import os

from flask import request
from flask_restful import Resource
from flask_restful.reqparse import RequestParser
from model import getParam

from app.model import getGroup
from app.tools.LibPdf import delete_file, upload_file, allowed_file


class PdfAPI(Resource):
    """
        Pdf Api Resource
    """

    def delete(self):
        parser = RequestParser()
        parser.add_argument('templateName', required=True, help="Template name is required !")
        args = parser.parse_args()

        if ".." in args:
            return {"msg": ".. not allowed in path"}, 400

        delete_file(os.path.join(getParam('TEMPLATES_DIRECTORY'), args['templateName']))

    def post(self):
        """
        Upload d'un template
        :return:
        """
        parser = RequestParser()
        parser.add_argument('groupeName', required=True, help="id/name groupe cannot be blank!")
        args = parser.parse_args()

        group = getGroup(args['groupe'])
        file = request.files['file']

        if file.filename == '':
            return {"message": "Fichier non trouve"}, 400

        if file and allowed_file(file.filename):
            upload_file(file, group["ressources_dir"])
