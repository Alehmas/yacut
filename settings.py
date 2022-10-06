import os

MAX_LEN_URL = 16
MIN_LEN_URL = 1
LEN_AUTO_NAME = 6


class Config(object):
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI', 'sqlite:///db.sqlite3')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY', 'SECRET_KEY')
