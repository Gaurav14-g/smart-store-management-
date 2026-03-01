#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
from dotenv import load_dotenv
load_dotenv(override=True)
import sys


def main():
    # Determine settings module based on database flags
    if os.getenv("USE_LOCAL") == "true":
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings.local')
    elif os.getenv("USE_DEV") == "true":
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings.development')
    elif os.getenv("USE_STAGE") == "true":
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings.stage')
    elif os.getenv("USE_PROD") == "true":
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings.production')
    else:
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings.local')

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
