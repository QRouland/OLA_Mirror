import os
from PyPDF2 import PdfFileReader, PdfFileMerger


def fusion_fichiers(chemin_merge_pdf, nom_merge_pdf, liste_de_pdf):
    """
    Permet de fusionner un ensemble de pdf
    :param chemin_merge_pdf: chemin ou l'on souhaite fusioner l'ensemble des pdf
    :param nom_merge_pdf: nom que l'on souhaite donner au fichier pdf final
    :param liste_de_pdf: liste de pdf avec leur chemin inclu
    :return:
    """
    merger = PdfFileMerger()
    for filename in liste_de_pdf:
        merger.append(PdfFileReader(os.path.join(filename), "rb"))
    merger.write(os.path.join(chemin_merge_pdf, nom_merge_pdf))


def get_pdf_from_directory(chemin_des_pdf):
    """
    Permet de récuperer l'ensemble des pdf d'un chemin
    :param chemin_des_pdf:
    :return:
    """
    return [f for f in os.listdir(chemin_des_pdf) if f.endswith("pdf")]
