from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from config import config_options

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()

# The name of the view to redirect to when login is required.
login_manager.login_view = "auth.login"
# The message to flash when a user is redirected to the login page.
login_manager.login_message = "Please sign in to access this page"


def create_app(config_name="development"):
    app = Flask(__name__)
    app.config.from_object(config_options[config_name])

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    from app.auth import bp as auth_bp

    app.register_blueprint(auth_bp, url_prefix="/auth")

    from app.main import bp as main_bp

    app.register_blueprint(main_bp)

    return app
