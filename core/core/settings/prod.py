import os
import io
from urllib.parse import urlparse
from .base import *

# Load settings from environment variable
import environ

env = environ.Env()
env.read_env(io.StringIO(env("APPLICATION_SETTINGS", None)))

# Basic Django settings
SECRET_KEY = env("SECRET_KEY")

# Ensure 'core' app is installed
if "core" not in INSTALLED_APPS:
    INSTALLED_APPS.append("core")

# Configure allowed hosts and CSRF trusted origins
ALLOWED_HOSTS = ["*"]  # Safe default for dev; tighten this if needed

# Debug mode
DEBUG = env.bool("DEBUG", default=False)

# Database configuration
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        # Use the service name 'db' from docker-compose.yml as the HOST
        'NAME': env('POSTGRES_DB'),
        'USER': env('POSTGRES_USER'),
        'PASSWORD': env('POSTGRES_PASSWORD'),
        'HOST': env('DB_HOST'), 
        'PORT': env('DB_PORT'),
    }
}

# Security settings
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_SSL_REDIRECT = True

SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = 'DENY'
SECURE_REFERRER_POLICY = 'same-origin'

# Trust X-Forwarded headers (important for Cloud Run / reverse proxies)
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
