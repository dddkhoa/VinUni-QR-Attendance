import logging
from tempfile import mkdtemp


class BaseConfig:
    LOGGING_LEVEL = logging.INFO

    SQLALCHEMY_DATABASE_URI = ""
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    APP_SECRET_KEY = ""

    CANVAS_URL = ""
    CANVAS_API_KEY = ""

    # TODO: for deployment, need API for input LTI_CLIENT_ID and LTI_DEPLOYMENT_ID
    LTI_URL = ""
    LTI_CLIENT_ID = ""
    LTI_DEPLOYMENT_ID = ""
    LTI_TOOL_NAME = ""

    CACHE_TYPE = "simple"
    CACHE_DIR = "lti_cache_dir"
    CACHE_DEFAULT_TIMEOUT = 3600
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    SESSION_TYPE = "filesystem"
    SESSION_FILE_DIR = mkdtemp()
    SESSION_COOKIE_NAME = "pylti1p3-flask-app-sessionid"
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SECURE = False  # should be True in case of HTTPS usage (production)
    SESSION_COOKIE_SAMESITE = None  # should be 'None' in case of HTTPS usage (production)
