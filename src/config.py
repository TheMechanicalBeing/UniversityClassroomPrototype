from os import path


class Config(object):
    SECRET_KEY = "SECRET"

    BASE_DIRECTORY = path.dirname(path.dirname(__file__))

    SQLALCHEMY_DATABASE_URI = "sqlite:///"
