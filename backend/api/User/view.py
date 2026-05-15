from django.contrib.auth.models import User
from api.User.serializers import UserSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny, IsAuthenticated

class UserViewset(ModelViewSet):
    queryset = User.objects.filter(is_superuser=False).exclude(username='admin')
    serializer_class = UserSerializer
    
    def get_permissions(self):
        if self.action == 'create':
            return [AllowAny()]
        return [IsAuthenticated()]