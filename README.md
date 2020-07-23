## Requirements

* Python 3.7+
* PostgreSQL

OR

* Docker
* Docker-compose

## Quick start

Don't forget to change settings in **services/settings.py**
Especially *DB_HOST* (If you want to run app locally, set this value to *localhost*)

- Docker way:
```
    docker-compose up
```

- Manual way

If you want manually install, then you have to create
database and set settings in file, specified above.

```
pip install -r requirements.txt
python services/main.py
```

## Project structure 

```
├── docker-compose.yml
├── Dockerfile
├── README.md
├── requirements.txt
└── services
    ├── dishes
    │   ├── db.py
    │   ├── __init__.py
    │   ├── middlewares.py
    │   ├── resources
    │   │   ├── default.jpg
    │   │   └── recipePhoto-03.jpg
    │   ├── routes.py
    │   ├── templates
    │   │   ├── base.html
    │   │   ├── delegate.html
    │   │   ├── error.html
    │   │   ├── index-4.html
    │   │   ├── index.html
    │   │   ├── recipe-page-2.html
    │   │   └── submit-recipe.html
    │   └── views.py
    ├── init.sql
    ├── main.py
    ├── settings.py
    └── tests
        └── tests.py

```
