# backend/dogger/settings/test.py
"""
Test settings for Django
IMPORTANT: This file overrides AUTH_USER_MODEL to use Django's default User
"""

# First, import everything from base
from .base import *

# CRITICAL: Override AUTH_USER_MODEL before Django loads
# This MUST come before any other imports or configurations
AUTH_USER_MODEL = 'auth.User'

# Override other settings for testing
SECRET_KEY = 'django-insecure-test-key-for-ci-cd-only-do-not-use-in-production'
DEBUG = True
ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'testserver', '*']

# Use SQLite in-memory for fast tests
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

# Disable password validators for easier testing
AUTH_PASSWORD_VALIDATORS = []

# CORS - allow everything in tests
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True

# Cache - use in-memory cache
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'test-cache',
    }
}

# Email - print to console
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Static/Media files
STATIC_ROOT = BASE_DIR / 'test_static'
MEDIA_ROOT = BASE_DIR / 'test_media'

# Logging - minimal for tests
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'ERROR',  # Only show errors in tests
    },
}

# Test runner
TEST_RUNNER = 'django.test.runner.DiscoverRunner'

# Security settings - relaxed for testing
SECURE_SSL_REDIRECT = False
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False

# Print confirmation that test settings are loaded
import sys
if 'test' in sys.argv or 'pytest' in sys.modules:
    print("🧪 Using TEST settings with AUTH_USER_MODEL = 'auth.User'")