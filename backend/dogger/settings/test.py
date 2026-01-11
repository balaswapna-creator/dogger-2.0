# backend/dogger/settings/test.py
"""
Django settings for testing environment
"""
from .base import *

# Override settings for testing

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Disable Cloudinary for tests
CLOUDINARY_STORAGE = {}

# Simple file storage for tests
DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'

ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'testserver']

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'corsheaders',
    # Your apps here
    # 'dogs',
    # 'users',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'dogger.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'dogger.wsgi.application'

# Database
# Use in-memory SQLite for faster tests
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

# Password validation - Disabled for testing
AUTH_PASSWORD_VALIDATORS = []

# Password validation - Disabled for testing
AUTH_PASSWORD_VALIDATORS = []

# CORS Settings - Allow all in testing
CORS_ALLOW_ALL_ORIGINS = True

# Cache - Use in-memory cache for testing
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-test-cache',
    }
}

# Email - Print to console in tests
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Logging - Minimal logging for tests
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
        'level': 'WARNING',  # Only show warnings and errors in tests
    },
}

# Testing
TEST_RUNNER = 'django.test.runner.DiscoverRunner'