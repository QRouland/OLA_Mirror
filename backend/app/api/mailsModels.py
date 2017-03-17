_NEW_USER = ("Votre compte OLA a été créé !", "Bonjour,<br/><p>Votre compte vient d'être créé dans l'Outil du "
                                              "Livret de l'Alternant dans le groupe #GROUPE. Vous pouvez dès "
                                              "maintenant créer un livret en vous rendant à l'adresse : <br/>"
                                              "<a href='#URL'>#URL</a></p><p>Bonne journée !</p>")


def getMailContent(mail_type, args):
    mail = None
    if mail_type == "NEW_USER":
        mail = _NEW_USER
        for key, value in args:
            mail[1].replace("#" + key, value)
    return mail
