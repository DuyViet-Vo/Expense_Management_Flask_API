from flask import Flask
from flask_cors import CORS

from app.blueprints import register_blueprints
from app.config import Config
from app.extensions import bcrypt, db, jwt, migrate


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    CORS(app, resources=Config.CORS_RESOURCES)

    # Khởi tạo extensions
    db.init_app(app)
    migrate.init_app(app, db)  # Kết nối Flask-Migrate với Flask app và db
    bcrypt.init_app(app)
    jwt.init_app(app)

    # Đăng ký các blueprint
    register_blueprints(app)

    return app


app = create_app()

with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)
