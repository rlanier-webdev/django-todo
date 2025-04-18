from .base import *

DEBUG = config('DEBUG', default=True, cast=bool)  # Read from .env, default to True
SECRET_KEY = config('SECRET_KEY')  # Read SECRET_KEY from .env

# ALLOWED_HOSTS should be read as a list (comma separated in .env)
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='127.0.0.1,localhost').split(',')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',  # SQLite for dev
        'NAME': BASE_DIR / config('DB_NAME', default='db.sqlite3'),  # Database name from .env
    }
}

# Optional: Debug context processor for template debugging
TEMPLATES[0]['OPTIONS']['context_processors'].insert(
    0, 'django.template.context_processors.debug'
)
