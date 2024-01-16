import random
from importlib import import_module

from canvasapi import Canvas
from flask import Flask
from flask_caching import Cache
from flask_cors import CORS
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from pylti1p3.contrib.flask import (
    FlaskOIDCLogin,
    FlaskMessageLaunch,
    FlaskRequest,
    FlaskCacheDataStorage,
)
from pylti1p3.exception import LtiException
from pylti1p3.tool_config import ToolConfDict

from main.commons.error_handlers import register_error_handlers
from main.config import config


class ReverseProxied(object):
    def __init__(self, app):
        self.app = app

    def __call__(self, environ, start_response):
        scheme = environ.get("HTTP_X_FORWARDED_PROTO")
        if scheme:
            environ["wsgi.url_scheme"] = scheme
        return self.app(environ, start_response)


app = Flask(__name__,
            static_url_path='',
            static_folder='./frontend/static',
            template_folder='./frontend/templates')
app.config.from_object(config)
app.wsgi_app = ReverseProxied(app.wsgi_app)

cache = Cache(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

canvas = Canvas(config.CANVAS_API_URL, config.CANVAS_API_KEY)
attendance_secret_key = random.randint(0, 1000000)

CORS(app, resources={r"/*": {"origins": "*"}})


def register_subpackages():
    from main import models

    for m in models.__all__:
        import_module("main.models." + m)

    import main.controllers  # noqa


register_subpackages()
register_error_handlers(app)
