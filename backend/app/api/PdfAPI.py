from flask_restful import Resource
from flask_restful.reqparse import RequestParser
from app.tools.LibPdf import delete_file
from model import getParam
from werkzeug.utils import secure_filename

from app.model import getGroup
from app.tools.LibPdf import upload_file, allowed_file
from app.api.LoginAPI import login_required

import os
import request

class PdfAPI(Resource):
    """
        Pdf Api Resource
    """
    @login_required()
    def delete(self):
        parser = RequestParser()
        parser.add_argument('templateName', required=True, help="Template name is required !")
        args = parser.parse_args()

        delete_file(os.path.join(getParam('TEMPLATES_DIRECTORY'), secure_filename(args['templateName'])))

    @login_required()
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
