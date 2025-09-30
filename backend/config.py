import os

class Config:
    # Secret & JWT
    SECRET_KEY = os.getenv("SECRET_KEY", "dev_secret_change_me")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "dev_jwt_secret_change_me")

    # DB: Use env DATABASE_URL if present (e.g., Render Postgres), else SQLite file
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///db.sqlite3")

    # SQLAlchemy URI normalization for Postgres (Render/Heroku style)
    if DATABASE_URL.startswith("postgres://"):
        DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

    SQLALCHEMY_DATABASE_URI = DATABASE_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # CORS
    CORS_ORIGINS = os.getenv("CORS_ORIGINS", "*")
