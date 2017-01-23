# -*- coding: utf-8 -*-
""" Script python qui remplie les pdf basés sur un template jinja. """

import os

from pdfjinja import PdfJinja

def remplirTemplate (dirname_template, pdf_template, dirname_output_file, pdf_output,dictionnaire):
    """
    Fonction qui permet de remplir un pdf template
    :param dirname_template: chemin du fichier de template
    :param pdf_template: nom du fichier de template
    :param dirname_output_file: chemin des pdf généré
    :param pdf_output: nom du fichier pdf à générer
    :param dictionnaire: dictionnaire contenant le nom des textfields des pdf ainsi que leurs valeurs
    :return:
    """
    template_pdf_file = os.path.join(dirname_template, pdf_template)
    template_pdf = PdfJinja(template_pdf_file)

    rendered_pdf = template_pdf(dictionnaire)

    output_file = os.path.join(dirname_output_file, pdf_output)
    rendered_pdf.write(open(output_file, 'wb'))
