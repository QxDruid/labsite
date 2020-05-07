import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    
    #database config
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or  'sqlite:///' + os.path.join(basedir, 'database/labsite.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False