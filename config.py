import os


class Config:
    CSRF_ENABLED = True
    SECRET_KEY = 'very-secret-key'

    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:postgres@localhost:5432/mediasite"
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_RECORD_QUERIES = True

    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')

    @staticmethod
    def init_app(app):
        pass


class DevConfig(Config):
    DEBUG = True


config = {
    'dev': DevConfig
}