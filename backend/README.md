# OLA Flask APP

BackEnd pour l'application du livret de l'altrenant

## Installer les dépendances

Required :

* python >= 3.4 with pip (Un VirtualEnv est conseillé !)
* bower >= 1.8

## Python

Si vous utiliser un virtualenv:
Creer et activerle virtualenv :

```
    cd backend
    virtualenv .
    bin/activate
```

Installer les dépendances via pip :
```
    pip install -r requirements/common.txt
```



## Run the App

### Fichier Configuration

Dans app/config.py:
* Configuration les parametres de la base de données
* Changer la SECRET_KEY en production

### Init App

First you need to create the db and seed it with an admin user (admin@admin.com/admin).

Migration database is handle via flask-migrate using alembic. 
See command available : 
```
    python manage.py db
```

#### Init db
Installet la derniere version de mariadb
Lancer le script :
```
    mysql -u root < ola_export.mysql
```


### Launch the App

#### For production server

```
    python manage.py runserver
```

#### For Debug server

```
    python manage.py -d runserver
```

## Run Tests

```
    python manage.py runtests
```
