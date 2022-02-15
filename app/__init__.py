from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail

mail = Mail()
db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    mail.init_app(app)

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)    

    from app.gallery import bp as gallery_bp
    app.register_blueprint(gallery_bp)
    
    from app.mailservice import bp as mailservice_bp
    app.register_blueprint(mailservice_bp)

    from app.admin import bp as admin_bp
    app.register_blueprint(admin_bp)
    
    return app

from app import db_models