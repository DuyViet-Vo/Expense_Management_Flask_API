import os
from datetime import timedelta


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "vdv18102001@")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URI", "postgresql+psycopg2://postgres:vdv1810@localhost:5432/test_3")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "voduyviet_flask_project")
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=30)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=7)
    CORS_RESOURCES = {
        r"/api/*": {
            "origins": ["http://localhost:3000"],
            "methods": ["GET", "POST"],
            "allow_headers": ["Content-Type", "Authorization"],
        }
    }
