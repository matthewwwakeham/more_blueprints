# app/__init__.py

# imports
import os
import logging
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

# Load environment variables from .env files
load_dotenv(dotenv_path='variables/.env')

# Initialize extensions
db = SQLAlchemy()

# Create app as a package
def create_app():
    app = Flask(__name__)

    # Secret and Config
    app.secret_key = os.getenv('SECRET_KEY')
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Initialize extensions
    db.init_app(app)

    # Setup logging
    setup_logging()

    # Register routes
    from .routes import chat_bp
    app.register_blueprint(chat_bp)

    return app

def setup_logging():
    '''Global Logging'''
    # Ensure logs directory exists
    if not os.path.exists('logs'):
        os.makedirs('logs')
    
    # Configure the root logger
    logging.basicConfig(
        filename='logs/app.log',
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    # Optional: Add console logging for development
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_formatter = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(console_formatter)

    # Attach console handler to the root logger
    root_logger = logging.getLogger()
    root_logger.addHandler(console_handler)