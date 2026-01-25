from .base import *

DEBUG = True
ALLOWED_HOSTS = ['*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': r'C:\Users\DR BALASUBRAMANI\Documents\Projects\dogger-2.0\backend\dogger\db.sqlite3',
    }
}

# Disable logging to avoid errors
LOGGING = {}