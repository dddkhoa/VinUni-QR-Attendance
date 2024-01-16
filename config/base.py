import logging


class BaseConfig:
    LOGGING_LEVEL = logging.INFO

    SQLALCHEMY_DATABASE_URI = "mysql+pymysql://root:123456@127.0.0.1/catalog"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = "VinUniQR"

    CANVAS_URL = "http://canvas.docker"
    CANVAS_API_KEY = ""

    # TODO: for deployment, need API for input LTI_CLIENT_ID and LTI_DEPLOYMENT_ID
    LTI_URL = "http://127.0.0.1:9001"
    LTI_CLIENT_ID = ""
    LTI_DEPLOYMENT_ID = ""

    GOOGLE_QR_API = "https://chart.googleapis.com/chart?\
        cht=qr&chs=300x300&chl={}&choe=UTF-8&chld=L|2"

    CACHE_TYPE = "filesystem"
    CACHE_DIR = "lti_cache_dir"
    CACHE_DEFAULT_TIMEOUT = 600
    DEBUG_TB_INTERCEPT_REDIRECTS = False
