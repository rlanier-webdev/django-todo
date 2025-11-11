#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os, io
import sys
import environ
from pathlib import Path

def main():
    """Run administrative tasks."""
    env = environ.Env()
    BASE_DIR = Path(__file__).resolve().parent.parent

    # Check for a local .env file
    env_path = BASE_DIR / '.env'
    if env_path.exists():
        print("Loading settings from local .env file.")
        env.read_env(str(env_path))
    elif os.environ.get("APPLICATION_SETTINGS"):
        print("Loading settings from APPLICATION_SETTINGS environment variable.")
        env.read_env(io.StringIO(os.environ.get("APPLICATION_SETTINGS")))
    else:
        print("No local .env or APPLICATION_SETTINGS found. Using default environment.")

    environment = env("ENVIRONMENT", default="development").lower()

    if environment == "production":
        print("Prod environment detected.")
        os.environ.setdefault('APPLICATION_SETTINGS_MODULE', 'core.settings.prod')
    else:
        print("Dev environment detected.")
        os.environ.setdefault('APPLICATION_SETTINGS_MODULE', 'core.settings.base')

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