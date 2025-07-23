# config\settings\prod.py
from .base import *
import environ
from pathlib import Path

# --- Base directory ---
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# --- Load .env.production ---
env = environ.Env(DEBUG=(bool, False))
env.read_env(BASE_DIR / "config" / "environment" / ".env.production")

# --- General settings ---
DEBUG = env.bool("DEBUG", default=False)
SECRET_KEY = env("SECRET_KEY")
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=[])

# --- Database config ---
DB_TYPE = env("DB_TYPE", default="postgres").strip().lower()
print(f"DB_TYPE loaded: '{DB_TYPE}'")
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
            "NAME": str(BASE_DIR / "db.sqlite3"),
        }
    }

elif DB_TYPE == "mongo":
    # Note: cần cấu hình riêng nếu dùng MongoDB
    DATABASES = {}
    MONGO_SETTINGS = {
        "HOST": env("MONGO_HOST", default="localhost"),
        "PORT": env.int("MONGO_PORT", default=27017),
        "NAME": env("MONGO_DB_NAME"),
    }

else:
    raise Exception(f"Unsupported DB_TYPE: {DB_TYPE}")
print("DATABASES config:", DATABASES)

# --- CORS config ---
CORS_ALLOW_ALL_ORIGINS = False
CORS_ALLOWED_ORIGINS = env.list("CORS_ALLOWED_ORIGINS", default=[])

# --- Email config ---
EMAIL_BACKEND = env("EMAIL_BACKEND", default="django.core.mail.backends.smtp.EmailBackend")
EMAIL_HOST = env("EMAIL_HOST")
EMAIL_PORT = env.int("EMAIL_PORT")
EMAIL_USE_TLS = env.bool("EMAIL_USE_TLS", default=True)
EMAIL_HOST_USER = env("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD")
DEFAULT_FROM_EMAIL = env("DEFAULT_FROM_EMAIL", default=EMAIL_HOST_USER)

