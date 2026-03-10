#!/usr/bin/env python
"""Quick script to check existing users in the database"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from django.contrib.auth.models import User

print("\n=== EXISTING USERS ===")
users = User.objects.all()

if not users.exists():
    print("❌ No users found in database!")
    print("\nCreate a superuser with:")
    print("python manage.py createsuperuser")
else:
    print(f"✅ Found {users.count()} user(s):\n")
    for user in users:
        print(f"Username: {user.username}")
        print(f"Email: {user.email}")
        print(f"Is Superuser: {user.is_superuser}")
        print(f"Is Active: {user.is_active}")
        print(f"Groups: {', '.join(user.groups.values_list('name', flat=True)) or 'None'}")
        print("-" * 40)
