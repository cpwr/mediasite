# -*- coding: utf-8 -*-

from flask import Flask

from flask.ext.bootstrap import Bootstrap
from flask.ext.mail import Mail
from flask.ext.moment import Moment
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.pagedown import PageDown
from flask.ext.wtf import CsrfProtect

import config

from app.lib.auth import AnonymousUser

app = Flask(__name__)
app.config.from_object(config)

bootstrap = Bootstrap(app)
mail = Mail(app)
moment = Moment(app)
db = SQLAlchemy(app)
pagedown = PageDown(app)
csrf = CsrfProtect(app)


def register_blueprints(app):

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .admin import admin as admin_blueprint
    app.register_blueprint(admin_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)


register_blueprints(app=app)
