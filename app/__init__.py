from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from config import Config
import logging
from pythonjsonlogger import jsonlogger
import os

db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
login.login_view = 'auth.login'

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)

    # Ensure the uploads directory exists
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    # Set up logging
    if not os.path.exists('logs'):
        os.mkdir('logs')
    
    logHandler = logging.FileHandler(app.config['LOG_FILE'])
    formatter = jsonlogger.JsonFormatter(
        '%(asctime)s %(levelname)s %(name)s %(message)s',
        timestamp=True
    )
    logHandler.setFormatter(formatter)
    app.logger.addHandler(logHandler)
    app.logger.setLevel(logging.INFO)

    # Register blueprints
    from app.routes import main, auth
    app.register_blueprint(main.bp)
    app.register_blueprint(auth.bp)

    # Register CLI commands
    from app.cli import init_db_command
    app.cli.add_command(init_db_command)

    # Log application startup
    app.logger.info('Application started', extra={
        'event_type': 'startup',
        'config_type': config_class.__name__
    })

    return app

from app import models