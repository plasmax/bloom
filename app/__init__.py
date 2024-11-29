from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config
import logging
from pythonjsonlogger import jsonlogger
import os

db = SQLAlchemy()
login = LoginManager()
login.login_view = 'auth.login'

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)
    login.init_app(app)

    # Ensure the uploads directory exists
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    # Set up logging
    if not os.path.exists('logs'):
        os.mkdir('logs')
    
    logHandler = logging.FileHandler(app.config['LOG_FILE'])
    logHandler.setFormatter(jsonlogger.JsonFormatter())
    app.logger.addHandler(logHandler)
    app.logger.setLevel(logging.INFO)

    # Register blueprints
    from app.routes import main, auth
    app.register_blueprint(main.bp)
    app.register_blueprint(auth.bp)

    return app

from app import models
