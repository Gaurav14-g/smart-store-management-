from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.conf import settings
import os

@api_view(['GET'])
@permission_classes([AllowAny])
def health_check(request):
    env_name = "LOCAL"
    if os.getenv("USE_LOCAL") == "true":
        env_name = "LOCAL"
    elif os.getenv("USE_DEV") == "true":
        env_name = "DEVELOPMENT"
    elif os.getenv("USE_STAGE") == "true":
        env_name = "STAGE"
    elif os.getenv("USE_PROD") == "true":
        env_name = "PRODUCTION"
    
    return Response({
        "status": "healthy",
        "environment": env_name,
        "message": "Django server is running"
    })
