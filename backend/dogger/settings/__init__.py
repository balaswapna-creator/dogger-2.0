import os
from .base import *

ENV = os.environ.get('DJANGO_ENV', 'development')

if ENV == 'production':
    from .production import *
elif ENV == 'test':
    from .test import *
else:
    from .development import *
