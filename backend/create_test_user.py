#!/usr/bin/env python
"""Create or reset test user for Smart Store"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from django.contrib.auth.models import User

# Test user credentials
username = 'admin'
password = 'admin123'
email = 'admin@example.com'

print("\n" + "="*50)
print("SMART STORE - Create/Reset Test User")
print("="*50 + "\n")

try:
    if User.objects.filter(username=username).exists():
        user = User.objects.get(username=username)
        user.set_password(password)
        user.is_active = True
        user.is_superuser = True
        user.is_staff = True
        user.email = email
        user.save()
        print(f"✅ User '{username}' already exists - Password RESET")
    else:
        user = User.objects.create_superuser(
            username=username,
            email=email,
            password=password
        )
        print(f"✅ Created new superuser '{username}'")
    
    print("\n" + "-"*50)
    print("LOGIN CREDENTIALS:")
    print("-"*50)
    print(f"Username: {username}")
    print(f"Password: {password}")
    print(f"Email: {email}")
    print("-"*50)
    
    print("\n✅ You can now login with these credentials!")
    print("\nFrontend: http://localhost:5173/signin")
    print("Backend: http://192.168.31.195:8000/admin/")
    print("\n" + "="*50 + "\n")
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    print("\nMake sure:")
    print("1. Database is running")
    print("2. Migrations are applied (python manage.py migrate)")
    print("3. .env file is configured correctly")
