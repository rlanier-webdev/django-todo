from .base import *

DEBUG = env('DEBUG')
SECRET_KEY = env('SECRET_KEY')

# ALLOWED_HOSTS should be read as a list (comma separated in .env)
ALLOWED_HOSTS = env.list('ALLOWED_HOSTS')

DATABASES = {
    'default': env.db(),  # Reads all DB config from environment
}

# Optional: Debug context processor for template debugging
TEMPLATES[0]['OPTIONS']['context_processors'].insert(
    0, 'django.template.context_processors.debug'
)
