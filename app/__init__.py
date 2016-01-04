# -*- coding: utf-8 -*-

from flask import Flask

from flask.ext.bootstrap import Bootstrap
from flask.ext.mail import Mail
from flask.ext.moment import Moment
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.pagedown import PageDown
from flask.ext.wtf import CsrfProtect
from flask_debugtoolbar import DebugToolbarExtension

from config import config

from app.lib.auth import AnonymousUser

bootstrap = Bootstrap()
mail = Mail()
moment = Moment()
db = SQLAlchemy()
pagedown = PageDown()
csrf = CsrfProtect()
toolbar = DebugToolbarExtension()


def register_blueprints(app):

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .admin import admin as admin_blueprint
    app.register_blueprint(admin_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)


def create_app(config_name):
    app = Flask(__name__)

    app.config.from_object(config[config_name])

    bootstrap.init_app(app=app)
    mail.init_app(app=app)
    moment.init_app(app=app)
    db.init_app(app=app)
    pagedown.init_app(app=app)
    csrf.init_app(app=app)
    toolbar.init_app(app=app)

    register_blueprints(app=app)

    return app
