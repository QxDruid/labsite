import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


class Config(object):
    
    DEBUG = os.environ.get('FLASK_DEBUG') or False
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'

    #database config
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or  'sqlite:///' + os.path.join(basedir, 'database/labsite.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
    BASE_DIR = os.path.dirname(PROJECT_ROOT)