import logging


class BaseConfig:
    LOGGING_LEVEL = logging.INFO

    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:123456@127.0.0.1/catalog"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = "VinUniQR"

    CANVAS_API_URL = "http://172.16.19.100"
    CANVAS_API_KEY = "HIfKcfbr4kBeSvZH43zRKnNrQdTjLlMMUEsfWffxYC6VzPTCt3zC5BdgVCfXUAbP"

    GOOGLE_QR_API = "https://chart.googleapis.com/chart?\
        cht=qr&chs=300x300&chl={}&choe=UTF-8&chld=L|2"
