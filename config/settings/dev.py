# config\settings\dev.py
from .base import *
import environ
from pathlib import Path

# --- Load .env file ---
env = environ.Env(DEBUG=(bool, True))
env.read_env(BASE_DIR / "config" / "environment" / ".env.dev")

# --- Debug mode ---
DEBUG = env.bool("DEBUG", default=True)

# --- Secret key ---
SECRET_KEY = env("SECRET_KEY", default="dev-secret-key")

# --- Allowed hosts ---
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=["localhost", "127.0.0.1"])

# --- Database selection ---
raw_db_type = env("DB_TYPE", default="postgres")
DB_TYPE = raw_db_type.strip().lower() if raw_db_type else "postgres"

if DB_TYPE == "postgres":
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": env("DB_NAME"),
            "USER": env("DB_USER"),
            "PASSWORD": env("DB_PASSWORD"),
            "HOST": env("DB_HOST"),
            "PORT": env("DB_PORT"),
        }
    }

elif DB_TYPE == "sqlite":
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            # Dùng DB_NAME nếu có, hoặc mặc định file db.sqlite3 trong BASE_DIR
            "NAME": env("DB_NAME", default=str(BASE_DIR / "db.sqlite3")),
        }
    }

elif DB_TYPE == "mongo":
    # Django không hỗ trợ MongoDB natively — cần thư viện bên ngoài
    DATABASES = {}
    MONGO_SETTINGS = {
        "HOST": env("MONGO_HOST", default="localhost"),
        "PORT": env.int("MONGO_PORT", default=27017),
        "NAME": env("MONGO_DB_NAME"),
    }

else:
    raise Exception(f"Unsupported DB_TYPE: {DB_TYPE}")

# --- CORS ---
CORS_ALLOW_ALL_ORIGINS = True

# --- Email backend for development ---
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

