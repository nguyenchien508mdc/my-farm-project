# config\settings\dev.py
from .base import *
import environ

BASE_DIR = Path(__file__).resolve().parent.parent.parent

env = environ.Env(DEBUG=(bool, True))
env.read_env(BASE_DIR / "config" / "environment" / ".env.dev")

DEBUG = env.bool("DEBUG", default=True)
SECRET_KEY = env("SECRET_KEY", default="dev-secret-key")
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS", default=["localhost", "127.0.0.1"])

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": env("DB_NAME", default="myfarm"),
        "USER": env("DB_USER", default="myfarm_user"),
        "PASSWORD": env("DB_PASSWORD", default="myfarm_pass"),
        "HOST": env("DB_HOST", default="db"),  # db là tên service docker-compose
        "PORT": env("DB_PORT", default="5432"),
    }
}

# CORS cho dev - cho phép tất cả origin
CORS_ALLOW_ALL_ORIGINS = True

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

