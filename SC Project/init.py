from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
from config import Config

db = SQLAlchemy()
login = LoginManager()
login.login_view = 'auth.login'
mail = Mail()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    login.init_app(app)
    mail.init_app(app)

    # Register blueprints
    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from app.patients import bp as patients_bp
    app.register_blueprint(patients_bp, url_prefix='/patients')

    from app.appointments import bp as appointments_bp
    app.register_blueprint(appointments_bp, url_prefix='/appointments')

    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    return app

from app import models