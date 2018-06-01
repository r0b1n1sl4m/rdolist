import os
from os.path import join, dirname

from dotenv import load_dotenv

# Load .env file
dotenv_path = join(dirname(__file__), '../.env')
load_dotenv(dotenv_path)


class Config(object):
    """Parent configuration class."""
    # Server
    SERVER_NAME = os.getenv('SERVER_NAME')

    # App
    DEBUG = False
    TESTING = False

    SECRET_KEY = os.getenv('SECRET_KEY')

    # DB
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Celery
    CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL')
    CELERY_RESULT_BACKEND = os.getenv('CELERY_RESULT_BACKEND')
    CELERY_ACCEPT_CONTENT = ['json']
    CELERY_TASK_SERIALIZER = 'json'
    CELERY_RESULT_SERIALIZER = 'json'

    # Flask-Mail
    MAIL_SERVER = os.getenv('MAIL_SERVER')
    MAIL_PORT = os.getenv('MAIL_PORT')
    MAIL_USE_TLS = os.getenv('MAIL_USE_TLS')
    MAIL_USE_SSL = os.getenv('MAIL_USE_SSL')
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER')


class DevelopmentConfig(Config):
    """Configurations for Development."""
    # App
    DEBUG = True


class TestingConfig(Config):
    """Configurations for Testing"""
    # Server
    SERVER_NAME = 'localhost:5000'

    # App
    TESTING = True
    DEBUG = True

    # DB
    SQLALCHEMY_DATABASE_URI = 'sqlite:///../test.db'


class ProductionConfig(Config):
    """Configurations for Production."""
    DEBUG = False
    TESTING = False


app_config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
}
