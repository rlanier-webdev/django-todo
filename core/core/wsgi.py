"""
WSGI config for core project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

environment = os.environ.get("ENVIRONMENT", "development").lower()

if environment == "production":
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings.prod')
else:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings.base')

application = get_wsgi_application()