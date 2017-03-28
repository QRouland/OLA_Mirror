import os

from PyPDF2 import PdfFileReader, PdfFileMerger
from pdfjinja import PdfJinja


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


def remplir_template(dirname_template, pdf_template, dirname_output_file, pdf_output, dictionnaire):
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


def allowed_file(filename):
    allowed_extensions = "pdf"
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed_extensions


def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file',
                                    filename=filename))
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <p><input type=file name=file>
         <input type=submit value=Upload>
    </form>
    '''
