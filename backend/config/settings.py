import os
from pathlib import Path

from dotenv import load_dotenv
from split_settings.tools import include

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get("SECRET_KEY")

DEBUG = os.environ.get("DEBUG")

ALLOWED_HOSTS = ['*']

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
CSRF_COOKIE_SETTINGS = True
USE_X_FORWARDED_HOST = True


include(
    'components/app_settings.py'
)


include(
    'components/db.py'
)

include(
    'components/celery_settings.py'
)


include(
    'components/auth.py'
)


include(
    'components/internationalization.py'
)

include(
    'components/static.py'
)


include(
    'components/celery_settings.py'
)

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

CORS_ALLOWED_ORIGINS = [
    "",
    ""
]
