import os


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "vdv18102001@")
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URI", "postgresql+psycopg2://postgres:vdv1810@localhost:5432/expense_management"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "voduyviet_flask_project")
