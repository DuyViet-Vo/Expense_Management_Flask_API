from flask import Flask

from .blueprints import register_blueprints
from .config import Config
from .extensions import bcrypt, db, jwt, migrate


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Khởi tạo extensions
    db.init_app(app)
    migrate.init_app(app, db)  # Kết nối Flask-Migrate với Flask app và db
    bcrypt.init_app(app)
    jwt.init_app(app)

    # Đăng ký các blueprint
    register_blueprints(app)

    return app
