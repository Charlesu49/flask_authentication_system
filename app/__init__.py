from flask import Flask, render_template
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from config import config
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail


moment = Moment()
db = SQLAlchemy()  # db = SQLAlchemy(session_options={"autoflush": False})
migrate = Migrate()
mail = Mail()


login_manager = LoginManager()
login_manager.login_view = 'auth.login'
# message flashed if user tries to access a protected route
login_manager.login_message = "User needs to be logged in to view this page"
login_manager.login_message_category = "warning"


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)

    migrate.init_app(app, db)
    moment.init_app(app)
    db.init_app(app)
    mail.init_app(app)
    login_manager.init_app(app)

    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    return app
