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
                                                       "maintenant l'activer en vous rendant à l'adresse : <br/>"
                                                       "<a href='#URL'>#URL</a></p><p>Bonne journée !</p>")

_RESP_OF_GROUP = (
    "Vous avez été ajouté à un groupe OLA !", "Bonjour,<br/><p>Votre compte vient d'être ajouté dans l'Outil du "
                                              "Livret de l'Alternant en tant que responsable du groupe <b>#GROUPE</b>. Vous pouvez dès "
                                              "maintenant y accéder en vous rendant à l'adresse : <br/>"
                                              "<a href='#URL'>#URL</a></p><p>Bonne journée !</p>")

_NEW_SEC_OF_GROUP = ("Votre compte OLA a été créé !", "Bonjour,<br/><p>Votre compte vient d'être créé dans l'Outil du "
                                                      "Livret de l'Alternant en tant que secrétaire du groupe <b>#GROUPE</b>. Vous pouvez dès "
                                                      "maintenant l'activer en vous rendant à l'adresse : <br/>"
                                                      "<a href='#URL'>#URL</a></p><p>Bonne journée !</p>")

_SEC_OF_GROUP = (
    "Vous avez été ajouté à un groupe OLA !", "Bonjour,<br/><p>Votre compte vient d'être ajouté dans l'Outil du "
                                              "Livret de l'Alternant en tant que secrétaire du groupe <b>#GROUPE</b>. Vous pouvez dès "
                                              "maintenant y accéder en vous rendant à l'adresse : <br/>"
                                              "<a href='#URL'>#URL</a></p><p>Bonne journée !</p>")

_NEW_ETUTOR_ADDED = ("Votre compte OLA a été créé !", "Bonjour,<br/><p>Votre compte vient d'être créé dans l'Outil du "
                                                      "Livret de l'Alternant de l'Université Toulouse Jean-Jaurès en tant que tuteur dans le groupe <b>#GROUPE</b>. Vous pouvez dès "
                                                      "maintenant l'activer en vous rendant à l'adresse : <br/>"
                                                      "<a href='#URL'>#URL</a></p><p>Bonne journée !</p>")

_ETUTOR_ADDED = (
    "Vous avez été déclaré comme tuteur dans OLA !", "Bonjour,<br/><p>Votre compte vient d'être ajouté dans l'Outil du "
                                                     "Livret de l'Alternant de l'Université Toulouse Jean-Jaurès en tant que tuteur dans le groupe <b>#GROUPE</b>. Vous pouvez dès "
                                                     "maintenant accéder à votre compte en vous rendant à l'adresse : <br/>"
                                                     "<a href='#URL'>#URL</a></p><p>Bonne journée !</p>")

_NEW_PERIOD = (
    "Nouvelle période ouverte dans OLA !", "Bonjour,<br/><p>Une nouvelle période vient d'être crée sur l'Outil du "
                                           "Livret de l'Alternant dans le groupe <b>#GROUPE</b>. Vous pouvez dès "
                                           "maintenant entrer vos commentaires en vous rendant à l'adresse : <br/>"
                                           "<a href='#URL'>#URL</a></p><p>Bonne journée !</p>")

_STUD_COMMENT_ADDED = (
    "Livret de l'alternant mis à jour !", "Bonjour,<br/><p>#ETUDIANT vient de mettre à jour son livret sur l'Outil du "
                                          "Livret de l'Alternant. Vous pouvez dès "
                                          "maintenant entrer à votre tour vos commentaires en vous rendant à l'adresse : <br/>"
                                          "<a href='#URL'>#URL</a></p><p>Bonne journée !</p>")

_ETUTOR_COMMENT_ADDED = (
    "Livret de l'alternant mis à jour !", "Bonjour,<br/><p>#TUTEUR vient de mettre à jour son livret sur l'Outil du "
                                          "Livret de l'Alternant. Vous pouvez visualiser ces modifcations"
                                          " en vous rendant à l'adresse : <br/>"
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
    elif mail_type == "NEW_ETUTOR_ADDED":
        mail = _NEW_ETUTOR_ADDED
    elif mail_type == "ETUTOR_ADDED":
        mail = _ETUTOR_ADDED
    elif mail_type == "NEW_PERIOD":
        mail = _NEW_PERIOD
    elif mail_type == "STUD_COMMENT_ADDED":
        mail = _STUD_COMMENT_ADDED
    elif mail_type == "ETUTOR_COMMENT_ADDED":
        mail = _ETUTOR_COMMENT_ADDED
    else:
        raise Exception("Unknown mail type : " + str(mail_type))

    obj = mail[0]
    content = str(mail[1])
    for key, value in args.items():
        content = content.replace("#" + key, value)
    return (obj, content)
