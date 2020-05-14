import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    FLASK_DEBUG = os.environ.get('FLASK_DEBUG') or False
    FLASK_PORT = os.environ.get('FLASK_PORT') or 8000
    FLASK_HOST = os.environ.get('FLASK_HOST') or '0.0.0.0'
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'

    #database config
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or  'sqlite:///' + os.path.join(basedir, 'database/labsite.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
    BASE_DIR = os.path.dirname(PROJECT_ROOT)