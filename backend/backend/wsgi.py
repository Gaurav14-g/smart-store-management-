import os
from dotenv import load_dotenv
load_dotenv(override=True)
from django.core.wsgi import get_wsgi_application

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

application = get_wsgi_application()
