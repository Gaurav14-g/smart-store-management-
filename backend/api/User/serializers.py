from rest_framework import serializers
from django.contrib.auth.models import User, Group, Permission
from django.contrib.auth.hashers import make_password
from api.UserProfile.model import UserProfile


class GroupDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['id', 'name']


class PermissionDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = ['id', 'name', 'codename']


class UserSerializer(serializers.ModelSerializer):
    groups = serializers.PrimaryKeyRelatedField(many=True, queryset=Group.objects.all())
    groups_detail = GroupDetailSerializer(source='groups', many=True, read_only=True)
    user_permissions_detail = serializers.SerializerMethodField()
    contact_no = serializers.IntegerField(required=False)

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'email', 'first_name', 'last_name',
                  'groups', 'groups_detail', 'user_permissions_detail',
                  'is_staff', 'is_active', 'contact_no']
        extra_kwargs = {'password': {'write_only': True}}

    def get_user_permissions_detail(self, instance):
        # Return all permissions from the user's groups
        perms = Permission.objects.filter(group__user=instance).distinct()
        return PermissionDetailSerializer(perms, many=True).data

    def to_representation(self, instance):
        # Get the original serialized data
        representation = super(UserSerializer, self).to_representation(instance)

        # Retrieve the UserProfile's contact_no and add it to the representation
        try:
            representation['contact_no'] = instance.userprofile.contact_no
        except UserProfile.DoesNotExist:
            representation['contact_no'] = None

        return representation

    def create(self, validated_data):
        groups_data = validated_data.pop('groups', [])
        contact_no = validated_data.pop('contact_no', None)

        # Hash the password before saving the user
        if 'password' in validated_data:
            validated_data['password'] = make_password(validated_data['password'])
        
        # Create the user
        user = super(UserSerializer, self).create(validated_data)
        
        # Set the groups for the user
        user.groups.set(groups_data)
        self._update_user_permissions(user)

        # Create the UserProfile linked to the user
        if contact_no is not None:
            UserProfile.objects.create(user=user, contact_no=contact_no)

        return user

    def update(self, instance, validated_data):
        groups_data = validated_data.pop('groups', None)  # None = not provided
        contact_no = validated_data.pop('contact_no', None)

        if 'password' in validated_data:
            validated_data['password'] = make_password(validated_data['password'])

        instance = super(UserSerializer, self).update(instance, validated_data)

        if groups_data is not None:  # Only update groups if explicitly sent
            instance.groups.set(groups_data)
            self._update_user_permissions(instance)

        if contact_no is not None:
            UserProfile.objects.update_or_create(user=instance, defaults={'contact_no': contact_no})

        return instance

    def _update_user_permissions(self, user):
        permissions = set()
        for group in user.groups.all():
            permissions.update(group.permissions.all())
        user.user_permissions.set(permissions)