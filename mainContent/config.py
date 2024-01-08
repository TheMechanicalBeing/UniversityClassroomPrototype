from pathlib import Path


class Config(object):
    SECRET_KEY = "SECRET"
    BASE_DIRECTORY = Path(__file__)
    SQLALCHEMY_DATABASE_URI = "sqlite:///"
