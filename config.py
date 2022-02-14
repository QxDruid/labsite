import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


class Config(object):
    
    DEBUG = os.environ.get('FLASK_DEBUG') or False
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'

    #database config
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
    BASE_DIR = os.path.dirname(PROJECT_ROOT)

    # mail config
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_DESTINATION = os.environ.get('MAIL_DESTINATION')