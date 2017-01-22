# OLA Flask APP

BackEnd pour l'application du livret de l'altrenant

## Installer les dépendances

Required :

* python >= 3.4 with pip (Un VirtualEnv est conseillé !)

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

Installer les dépendances via pip pour les tests :
```
    pip install -r requirements/test.txt
```


## Run the App

### Fichier Configuration

Copier le fichier app/config.py.example en app/config.py et configurer avec vos parametres

Principalement:
* Configuration des paramètres de la base de données
* Changement de la SECRET_KEY en production


### Init db
Installez la dernière version de MariaDB.

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
