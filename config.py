import os
basedir = os.path.abspath(os.path.dirname(__file__))


# The Config base class contains settings that are common to all configurations; the different
# subclasses define settings that are specific to a configuration. Additional configurations can
# be added ass needed.
class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    DEBUG = True
    APP_ADMIN = ['john', 'emeka', 'ayomide']
    SQLALCHEMY_DATABASE_URI = "sqlite:///database.db"
    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_SUBJECT_PREFIX = "[CU]"
    MAIL_SENDER = os.environ.get('MAIL_SENDER')
    MAIL_ADMIN = "CHARLES"


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'test.db')


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'prod.db')


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,

    'default': DevelopmentConfig
}
