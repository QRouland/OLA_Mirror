_NEW_STUD_OF_GROUP = ("Votre compte OLA a été créé !", "Bonjour,<br/><p>Votre compte vient d'être créé dans l'Outil du "
                                                       "Livret de l'Alternant dans le groupe <b>#GROUPE</b>. Vous pouvez dès "
                                                       "maintenant l'activer, puis créer un livret en vous rendant à l'adresse : <br/>"
                                                       "<a href='#URL'>#URL</a></p><p>Bonne journée !</p>")

_STUD_OF_GROUP = (
    "Vous avez été ajouté à un groupe OLA !", "Bonjour,<br/><p>Votre compte vient d'être ajouté dans l'Outil du "
                                              "Livret de l'Alternant au groupe <b>#GROUPE</b>. Vous pouvez dès "
                                              "maintenant créer un livret en vous rendant à l'adresse : <br/>"
                                              "<a href='#URL'>#URL</a></p><p>Bonne journée !</p>")

_NEW_RESP_OF_GROUP = ("Votre compte OLA a été créé !", "Bonjour,<br/><p>Votre compte vient d'être créé dans l'Outil du "
                                                       "Livret de l'Alternant en tant que responsable du groupe <b>#GROUPE</b>. Vous pouvez dès "
                                                       "maintenant l'activer, en vous rendant à l'adresse : <br/>"
                                                       "<a href='#URL'>#URL</a></p><p>Bonne journée !</p>")

_RESP_OF_GROUP = (
    "Vous avez été ajouté à un groupe OLA !", "Bonjour,<br/><p>Votre compte vient d'être ajouté dans l'Outil du "
                                              "Livret de l'Alternant en tant que responsable du groupe <b>#GROUPE</b>. Vous pouvez dès "
                                              "maintenant y accéder en vous rendant à l'adresse : <br/>"
                                              "<a href='#URL'>#URL</a></p><p>Bonne journée !</p>")

_NEW_SEC_OF_GROUP = ("Votre compte OLA a été créé !", "Bonjour,<br/><p>Votre compte vient d'être créé dans l'Outil du "
                                                      "Livret de l'Alternant en tant que secrétaire du groupe <b>#GROUPE</b>. Vous pouvez dès "
                                                      "maintenant l'activer, en vous rendant à l'adresse : <br/>"
                                                      "<a href='#URL'>#URL</a></p><p>Bonne journée !</p>")

_SEC_OF_GROUP = (
    "Vous avez été ajouté à un groupe OLA !", "Bonjour,<br/><p>Votre compte vient d'être ajouté dans l'Outil du "
                                              "Livret de l'Alternant en tant que secrétaire du groupe <b>#GROUPE</b>. Vous pouvez dès "
                                              "maintenant y accéder en vous rendant à l'adresse : <br/>"
                                              "<a href='#URL'>#URL</a></p><p>Bonne journée !</p>")


def getMailContent(mail_type, args):
    if mail_type == "NEW_STUD_OF_GROUP":
        mail = _NEW_STUD_OF_GROUP
    elif mail_type == "STUD_OF_GROUP":
        mail = _STUD_OF_GROUP
    elif mail_type == "NEW_RESP_OF_GROUP":
        mail = _NEW_RESP_OF_GROUP
    elif mail_type == "RESP_OF_GROUP":
        mail = _RESP_OF_GROUP
    elif mail_type == "NEW_SEC_OF_GROUP":
        mail = _NEW_SEC_OF_GROUP
    elif mail_type == "SEC_OF_GROUP":
        mail = _SEC_OF_GROUP
    else:
        raise Exception("Unknown mail type !")

    for key, value in args.items():
        mail[1].replace("#" + key, value)
    return mail
