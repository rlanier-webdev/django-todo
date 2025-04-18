"""
ASGI config for core project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""

import os
from decouple import config
from django.core.asgi import get_asgi_application

environment = config("ENVIRONMENT", default="development").lower()

if environment == "production":
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings.prod')
else:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings.dev')

application = get_asgi_application()
