# OLA Flask APP

BackEnd pour l'application du livret de l'altrenant

## Installer les dépendances

Required :

* Python >= 3.4 with pip (Un VirtualEnv est conseillé !)

## Python

Si vous utilisez un virtualenv :

Créer et activer le virtualenv :

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
* Configuration les paramètres de la base de données
* Changer la SECRET_KEY en production

### Init App

First you need to create the db and seed it with an admin user (admin@admin.com/admin).

Migration database is handle via flask-migrate using alembic. 
See command available : 
```
    python manage.py db
```

#### Init db
Installez la dernière version de MariaDB:

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
