#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import environ
import os, io
import sys

from pathlib import Path

def main():
    """Run administrative tasks."""
    env = environ.Env()
    BASE_DIR = Path(__file__).resolve().parent.parent

    # ... (env loading logic remains the same)
    
    environment = env("ENVIRONMENT", default="development").lower()
    
    settings_module = None # Initialize a variable to hold the settings path

    if environment == "production":
        print("Prod environment detected.")
        settings_module = 'core.settings.prod'
    else:
        print("Dev environment detected.")
        settings_module = 'core.settings.base'

    # Set the standard Django environment variable directly
    if settings_module:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', settings_module)
        print(f"Using settings module: {settings_module}")

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Make sure it's installed and available on your PYTHONPATH environment variable."
            "Did you forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()