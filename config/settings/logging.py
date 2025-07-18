# config\settings\logging.py
import os
from pathlib import Path

# Gốc dự án
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Thư mục chứa log
LOG_DIR = BASE_DIR / 'logs'
LOG_DIR.mkdir(exist_ok=True)

# DEBUG được lấy từ môi trường hoặc mặc định là False
DEBUG = os.environ.get("DEBUG", "False") == "True"

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,

    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} [{name}] {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname}: {message}',
            'style': '{',
        },
    },

    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
        'file_debug': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': LOG_DIR / 'django_debug.log',
            'maxBytes': 5 * 1024 * 1024,  # 5MB
            'backupCount': 3,
            'formatter': 'verbose',
        },
        'file_error': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': LOG_DIR / 'django_errors.log',
            'formatter': 'verbose',
        },
    },

    'loggers': {
        'django': {
            'handlers': ['console', 'file_debug'] if DEBUG else ['file_error'],
            'level': 'DEBUG' if DEBUG else 'ERROR',
            'propagate': True,
        },
        'myfarm': {
            'handlers': ['console', 'file_debug'],
            'level': 'DEBUG',
            'propagate': False,
        },
    }
}
