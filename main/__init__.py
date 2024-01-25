import atexit
import random
from importlib import import_module

from apscheduler.schedulers.background import BackgroundScheduler
from canvasapi import Canvas
from flask import Flask
from flask_caching import Cache
from flask_cors import CORS
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy


from main.commons.error_handlers import register_error_handlers
from main.config import config
from main.libs.qr import generate_secret_key


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
            static_folder='../frontend/static',
            template_folder='../frontend/templates')
app.config.from_object(config)
app.secret_key = app.config["APP_SECRET_KEY"]
app.wsgi_app = ReverseProxied(app.wsgi_app)

cache = Cache(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

canvas = Canvas(config.CANVAS_URL, config.CANVAS_API_KEY)

CORS(app, resources={r"/*": {"origins": "*"}})


def register_subpackages():
    from main import models

    for m in models.__all__:
        import_module("main.models." + m)

    import main.controllers  # noqa


def update_secret_key():
    global qr_secret_key
    qr_secret_key = generate_secret_key()


qr_secret_key = generate_secret_key()
scheduler = BackgroundScheduler()
scheduler.add_job(func=update_secret_key, trigger="interval", seconds=5)
scheduler.start()


@app.before_first_request
def start_scheduler():
    if not scheduler.running:
        scheduler.start()


@atexit.register
def shutdown_scheduler():
    scheduler.shutdown()


register_subpackages()
register_error_handlers(app)
