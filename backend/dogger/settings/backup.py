from .base import *

DEBUG = True
ALLOWED_HOSTS = ['*']

# Put your OLD database URL here
DATABASES = {
    'default': dj_database_url.parse('postgresql://OLD_DATABASE_URL_HERE')
}