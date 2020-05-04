from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# create instance
db = SQLAlchemy()
login_manager = LoginManager()


def register_extensions(app):
    """Register extensions"""

    # Flask-SQLAlchemy
    db.init_app(app)

    # Flask-Login
    login_manager.init_app(app)

    if app.config["TEST"]:
        pass

    return None
