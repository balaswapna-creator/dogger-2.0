#!/usr/bin/env python
"""
Verify test settings are configured correctly
Run this before running tests to check configuration
"""
import os
import sys
import django

# Set the settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dogger.settings.test')

print("=" * 60)
print("Verifying Test Settings Configuration")
print("=" * 60)
print()

try:
    # Setup Django
    django.setup()
    from django.conf import settings
    
    print("✅ Django setup successful")
    print()
    
    # Check AUTH_USER_MODEL
    auth_user_model = settings.AUTH_USER_MODEL
    print(f"👤 AUTH_USER_MODEL: {auth_user_model}")
    
    if auth_user_model == 'auth.User':
        print("   ✅ Using Django's default User model (correct for tests)")
    elif auth_user_model == 'clinic.User':
        print("   ❌ Still using clinic.User - test.py override not working!")
        print("   🔧 Fix: Ensure test.py has: AUTH_USER_MODEL = 'auth.User'")
        sys.exit(1)
    else:
        print(f"   ⚠️  Using custom model: {auth_user_model}")
    
    print()
    
    # Check if clinic is in INSTALLED_APPS
    print("📦 Checking INSTALLED_APPS:")
    if 'clinic' in settings.INSTALLED_APPS:
        print("   ⚠️  'clinic' is in INSTALLED_APPS")
        if auth_user_model == 'clinic.User':
            print("   This is okay if the clinic app exists")
    else:
        print("   ✅ 'clinic' is NOT in INSTALLED_APPS (good for basic tests)")
    
    print()
    
    # Check database
    db_engine = settings.DATABASES['default']['ENGINE']
    db_name = settings.DATABASES['default'].get('NAME', 'N/A')
    print(f"🗄️  Database:")
    print(f"   Engine: {db_engine}")
    print(f"   Name: {db_name}")
    
    if db_name == ':memory:':
        print("   ✅ Using in-memory SQLite (fast for tests)")
    
    print()
    
    # Test importing the User model
    print("🧪 Testing User model import:")
    try:
        from django.contrib.auth import get_user_model
        User = get_user_model()
        print(f"   ✅ User model loaded: {User}")
        print(f"   Model location: {User.__module__}.{User.__name__}")
    except Exception as e:
        print(f"   ❌ Failed to load User model: {e}")
        sys.exit(1)
    
    print()
    print("=" * 60)
    print("✅ All checks passed! You can now run tests:")
    print("   python manage.py test --settings=dogger.settings.test")
    print("=" * 60)
    
except Exception as e:
    print(f"❌ Error: {e}")
    print()
    import traceback
    traceback.print_exc()
    sys.exit(1)