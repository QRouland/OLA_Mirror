from flask_restful import Resource

from app.model import *
from app.tools.LibPdf import fusion_fichiers


class ExportPdfAPI(Resource):
    def get(self, uid=0, gid=0, name=""):
        if uid > 0:

            user = getUser(uid=uid)

            group = getGroup(gid)

            if user is None:
                return {"ERROR": "The user with id " + str(gid) + " does not exists !"}, 400

            prenom = user["name"].split(" ", 1)
            nom = user["name"].split(" ", 2)

            group["name"]

            annee1 = group["year"]
            annee2 = int(group["year"]) + 1
            promo = group["class_short"]

            group["class_long"]
            group["departement"]
            group["resp_id"]
            group["sec_id"]
            group["ressources_dir"]

            self.data = {
                'page1.nom_master': 'Renan',
                'page1.nom_complet_master': 'Husson',
                'page1.annee_1': 'Husson',
                'page1.annee_2': 'Jean Jaures',
                'page1.nom_prenom': 'Panda',
                'page1.email': 'Panda',
                'page1.telephone': 'Panda',
                'page1.entreprise': 'Panda',
                'page1.tuteur_pedagogique': 'Panda',
                'page1.tuteur_entreprise': 'Panda',
                'page2.type_contrat_apprentissage': True,
                'page2.type_contrat_professionnalisation': True,
                'page2.type_contrat_stage': True,
                'page2.debut_contrat': 'Panda',
                'page2.fin_contrat': 'Panda',
                'page2.telephone': 'Panda',
                'page2.email': 'Panda',
                'page2.compostant_formation': 'Panda',
                'page2.responsable_pedagogique_formation': 'Panda',
                'page2.tel_responsable_pedagogique_formation': 'Panda',
                'page2.mail_responsable_pedagogique_formation': 'Panda',
                'page2.tel_tuteur_pedagogique': 'Panda',
                'page2.mail_tuteur_pedagogique': 'Panda',
                'page2.tuteur_entreprise': 'Panda',
                'page2.entreprise': 'Panda',
                'page2.adresse_entreprise': 'Panda',
                'page2.tel_tuteur_entreprise': 'Panda',
                'page2.mail_tuteur_entreprise': 'Panda',
                'page4.poste_occupe': 'Panda',
                'page4.poste_occupe_2': 'Panda',
                'PEntreprise.n_periode': 'Panda',
                'PEntreprise.debut_periode': 'Panda',
                'PEntreprise.fin_periode': 'Panda',
                'PEntreprise.travaux_entreprise': 'Panda',
                'PEntreprise.remarque_tuteur': 'Panda',
                'pagePFormation.n_periode': 'Panda',
                'pagePFormation.bilan_periode': 'Panda',

            }

            pdf_fusion = ["/page1.pdf", "/page2.pdf"]
            chemin_pdf = "/tmp"

            nom_pdf = "Livret_Alternant_BOB_Armandeau.pdf"

            fusion_fichiers(chemin_pdf, nom_pdf, pdf_fusion)

            # Prenom NOM
            # remplir_template()
