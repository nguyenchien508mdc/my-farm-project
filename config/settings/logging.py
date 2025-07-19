import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
LOG_DIR = BASE_DIR / 'logs'
LOG_DIR.mkdir(exist_ok=True)

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
            'level': 'INFO',
        },
        'file_debug': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',  
            'filename': LOG_DIR / 'django_debug.log',
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
        'django.server': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
        'django.db.backends': {
            'level': 'ERROR',  
            'handlers': ['console'] if DEBUG else ['file_error'],
            'propagate': False,
        },
        'django': {
            'handlers': ['console', 'file_debug'] if DEBUG else ['file_error'],
            'level': 'DEBUG' if DEBUG else 'ERROR',
            'propagate': True,
        },
        'myfarm': {
            'handlers': ['console', 'file_debug'] if DEBUG else ['file_error'],
            'level': 'DEBUG' if DEBUG else 'ERROR',
            'propagate': False,
        },
    }
}
