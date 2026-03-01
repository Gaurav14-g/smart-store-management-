import os
from dotenv import load_dotenv
load_dotenv(override=True)

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

import django
django.setup()

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import api.Websocket.routings

application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    'websocket': AuthMiddlewareStack(
        URLRouter(
            api.Websocket.routings.websocket_urlpatterns
        )
    ),
})
