import os
from PyPDF2 import PdfFileReader, PdfFileMerger


def fusion_fichiers(chemin_des_pdf, chemin_merge_pdf, nom_merge_pdf):
    pdf_files = [f for f in os.listdir(chemin_des_pdf) if f.endswith("pdf")]
    merger = PdfFileMerger()
    for filename in pdf_files:
        merger.append(PdfFileReader(os.path.join(chemin_des_pdf, filename), "rb"))
    merger.write(os.path.join(chemin_merge_pdf, nom_merge_pdf))
