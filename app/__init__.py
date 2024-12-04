from flask import Flask
from .extensions import db, migrate, bcrypt, jwt
from .config import Config
from .blueprints import register_blueprints

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
