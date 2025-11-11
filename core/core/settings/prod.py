import os
import io
from urllib.parse import urlparse
from .base import *

# Load settings from environment variable
import environ

env = environ.Env()
env.read_env(io.StringIO(os.environ.get("APPLICATION_SETTINGS", None)))

# Basic Django settings
SECRET_KEY = env("SECRET_KEY")

# Ensure 'core' app is installed
if "core" not in INSTALLED_APPS:
    INSTALLED_APPS.append("core")

# Configure allowed hosts and CSRF trusted origins
CLOUDRUN_SERVICE_URLS = env("CLOUDRUN_SERVICE_URLS", default=None)
if CLOUDRUN_SERVICE_URLS:
    urls = CLOUDRUN_SERVICE_URLS.split(",")
    CSRF_TRUSTED_ORIGINS = urls
    ALLOWED_HOSTS = [urlparse(url).netloc for url in urls]
else:
    ALLOWED_HOSTS = ["*"]  # Safe default for dev; tighten this if needed

# Debug mode
DEBUG = env.bool("DEBUG", default=False)

# Database configuration
DATABASES = {
    "default": env.db()
}

# Adjust if using Cloud SQL Auth Proxy
if os.getenv("USE_CLOUD_SQL_AUTH_PROXY", None):
    DATABASES["default"]["HOST"] = "127.0.0.1"
    DATABASES["default"]["PORT"] = 5432

# Static files (using Google Cloud Storage)
GS_BUCKET_NAME = env("GS_BUCKET_NAME")
STATICFILES_DIRS = []
GS_DEFAULT_ACL = "publicRead"

STORAGES = {
    "default": {
        "BACKEND": "storages.backends.gcloud.GoogleCloudStorage",
    },
    "staticfiles": {
        "BACKEND": "storages.backends.gcloud.GoogleCloudStorage",
    },
}

# Static files URL (IMPORTANT if serving static assets from GCS)
STATIC_URL = f"https://storage.googleapis.com/{GS_BUCKET_NAME}/"

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
