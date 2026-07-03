from .base import *

# Development settings
DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1', 'localhost']

import sys

if 'test' in sys.argv:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
else:
    # PostgreSQL Database configuration (Option A)
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'neondb',
            'USER': 'neondb_owner',
            'PASSWORD': 'npg_SDTLZ5AgIqx0',
            'HOST': 'ep-shy-math-airyg9if-pooler.c-4.us-east-1.aws.neon.tech',
            'PORT': '5432',
            'OPTIONS': {
                'sslmode': 'require',
            },
        }
    }

# Development email backend is defined dynamically in base.py
