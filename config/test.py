from .local import Config as _Config


class Config(_Config):
    TESTING = True

    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:123456@127.0.0.1/catalog_test"
