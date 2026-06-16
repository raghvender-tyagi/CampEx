from .base import *

# Development settings
DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1', 'localhost']

# SQLite Database local usage
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Development email backend
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
