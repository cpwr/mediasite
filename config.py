# coding: utf-8

import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:

    WTF_CSRF_ENABLED = True
    SECRET_KEY = 'very-secret-key'

    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:postgres@localhost:5432/mediasite"
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_RECORD_QUERIES = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')

    UPLOAD_FOLDER = os.path.join(basedir, 'app/media/')

    MAX_CONTENT_LENGTH = 75 * 1024 * 1024
    ALLOWED_FILE_EXTENSIONS = set(
        [
            'xpm', 'pgm', 'webp', 'pbm', 'rgb', 'icb', 'ppm',
            'bmp', 'pic', 'eps', 'jp2', 'tif', 'ico', 'odt',
            'fodt', 'uot', 'dot', 'xml', 'html', 'rtf', 'png',
            'jpg', 'jpeg', 'gif', 'txt', 'doc', 'docx', 'opt', 'pdf',
            'xls', 'xslt', 'mp3'
        ]
    )

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):

    DEBUG = True
    SERVER_NAME = '127.0.0.1:5000'


class ProductionConfig(Config):

    DEBUG = False


config = dict(
    dev=DevelopmentConfig,
    production=ProductionConfig,
)
