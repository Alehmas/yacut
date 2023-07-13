# Yacut

##  Description
Yacut is a link shortening service that associates a long user link with a short one. A short link can be offered by the user himself, or the service will generate it on its own.

In other words, with the help of this service, the user can turn a long and inconvenient link like "https://flask.palletsprojects.com/en/2.2.x/changes/#version-2-0-0" into a short one - "http:/ /localhost/ver2". After creating a short link, when you click on it, you are redirected to the original address.

In addition to working in a browser with a graphical interface, an API is available to everyone, duplicating the entire functionality of the service.

##  Technologies used
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white) ![Flask](https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white) ![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-6d8a7f?style=for-the-badge) ![HTML](https://img.shields.io/badge/HTML-239120?style=for-the-badge&logo=html5&logoColor=white)

## Installation

1. Clone the repository
```bash
git clone git@github.com:Alehmas/yacut.git
```

2. Activate venv and install dependencies
```bash
python -m venv venv
source venv/Scripts/activate
pip install -r requirements.txt
```

3. Create an .env file in the root directory with the following content
```bash
FLASK_APP=yacut
FLASK_ENV=development или production
DATABASE_URI=sqlite:///db.sqlite3
SECRET_KEY=<ваш_секретный_ключ>
```

4. Launch the Flask interactive shell and create the database.
```bash
flask shell
>>> from yacut import db       
>>> db.create_all()
>>> exit()
```

## Control
To run locally, run the command
```bash
flask run
```

### The service will be launched and available at the following addresses:

- [http://localhost/](http://localhost/) - main page of the service.
    - If you do not fill in the field for a short link, it will be generated automatically.
    - A short link should be no longer than 16 characters (numbers and Latin letters in any case).

- [http://localhost/api/id/](http://localhost/api/id/) - endpoint that accepts POST requests.
    - POST request scheme
    ```
    {
        "url": "string",
        "custom_id": "string"  ## необязательное поле
    }
    ```
    - POST response scheme
    ```
    {
        "url": "string",
        "short_link": "string"
    }
    ```

- [http://localhost/api/id/short_id/](http://localhost/api/id/short_id/) - endpoint that accepts GET requests.
    In the address, instead of <short_id>, the entered or generated short link must be indicated.
    - GET response scheme
    ```
    {
        "url": "string"
    }
    ```

## Specification
Full API specification is available in the repository - file openapi.yml

## Authors
- [Aleh Maslau](https://github.com/Alehmas)