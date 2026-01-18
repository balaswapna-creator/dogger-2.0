"""
Production settings for Dogger 2.0
CRITICAL FIX: Properly configure ALLOWED_HOSTS for Render deployment
"""

from .base import *
import os
import dj_database_url

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# CRITICAL: ALLOWED_HOSTS Configuration
# This must include your Render domain to avoid DisallowedHost errors
ALLOWED_HOSTS = [
    'dogger2-backend.onrender.com',
    '.onrender.com',
    'localhost',
    '127.0.0.1',
]

# Database - Use DATABASE_URL from Render or fallback to SQLite
if os.environ.get('DATABASE_URL'):
    # Production: Use PostgreSQL from Render
    DATABASES = {
        'default': dj_database_url.config(
            default=os.environ.get('DATABASE_URL'),
            conn_max_age=600,
            conn_health_checks=True,
        )
    }
else:
    # Fallback: Use SQLite (for development/testing)
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }

# CORS Settings
CORS_ALLOWED_ORIGINS = [
    'https://dogger2-frontend.onrender.com',
]

CORS_ALLOW_CREDENTIALS = True

# REST Framework - DISABLE rate limiting temporarily for testing
REST_FRAMEWORK = {
    **REST_FRAMEWORK,  # Keep existing settings from base.py
    'DEFAULT_THROTTLE_CLASSES': [],  # Disable all throttling
    'DEFAULT_THROTTLE_RATES': {
        'anon': None,      # No limit
        'user': None,      # No limit
        'login': None,     # No limit
    }
}

# Disable rate limiting middleware temporarily
MIDDLEWARE = [item for item in MIDDLEWARE if 'RateLimitMiddleware' not in item]

# Security Settings
SECURE_SSL_REDIRECT = False  # Render handles SSL
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Cloudinary (if used)
if os.environ.get('CLOUDINARY_CLOUD_NAME'):
    CLOUDINARY_STORAGE = {
        'CLOUD_NAME': os.environ.get('CLOUDINARY_CLOUD_NAME'),
        'API_KEY': os.environ.get('CLOUDINARY_API_KEY'),
        'API_SECRET': os.environ.get('CLOUDINARY_API_SECRET'),
    }
    DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

# Redis Cache (if configured)
if os.environ.get('REDIS_URL'):
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.redis.RedisCache',
            'LOCATION': os.environ.get('REDIS_URL'),
        }
    }

# Logging
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}

print(f"[PRODUCTION] ALLOWED_HOSTS = {ALLOWED_HOSTS}")
print(f"[PRODUCTION] DEBUG = {DEBUG}")
print(f"[PRODUCTION] Rate limiting: DISABLED")