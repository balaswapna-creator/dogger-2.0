#!/usr/bin/env python
"""
Configuration Test Script
Tests environment configuration loading and validation
"""

import os
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dogger.settings')
import django
django.setup()

from clinic.config import config, is_production, is_development
from django.conf import settings


def test_environment_detection():
    """Test environment detection"""
    print("=" * 70)
    print("🧪 ENVIRONMENT DETECTION TEST")
    print("=" * 70)
    print()
    
    print(f"Environment: {config.get('ENVIRONMENT', 'unknown')}")
    print(f"Is Production: {is_production()}")
    print(f"Is Development: {is_development()}")
    print(f"DEBUG Mode: {settings.DEBUG}")
    print()


def test_database_config():
    """Test database configuration"""
    print("=" * 70)
    print("💾 DATABASE CONFIGURATION TEST")
    print("=" * 70)
    print()
    
    db_config = settings.DATABASES['default']
    print(f"Database Engine: {db_config['ENGINE']}")
    print(f"Database Name: {db_config['NAME']}")
    print()


def test_security_config():
    """Test security configuration"""
    print("=" * 70)
    print("🔒 SECURITY CONFIGURATION TEST")
    print("=" * 70)
    print()
    
    print(f"SECRET_KEY Length: {len(settings.SECRET_KEY)} chars")
    print(f"SECRET_KEY Set: {'✅' if settings.SECRET_KEY and len(settings.SECRET_KEY) > 20 else '❌'}")
    print()
    print(f"CORS Allowed Origins: {settings.CORS_ALLOWED_ORIGINS}")
    print(f"CSRF Trusted Origins: {settings.CSRF_TRUSTED_ORIGINS}")
    print()
    print(f"Session Cookie Secure: {settings.SESSION_COOKIE_SECURE}")
    print(f"CSRF Cookie Secure: {settings.CSRF_COOKIE_SECURE}")
    print()


def test_jwt_config():
    """Test JWT configuration"""
    print("=" * 70)
    print("🔑 JWT CONFIGURATION TEST")
    print("=" * 70)
    print()
    
    jwt_config = settings.SIMPLE_JWT
    print(f"Access Token Lifetime: {jwt_config['ACCESS_TOKEN_LIFETIME']}")
    print(f"Refresh Token Lifetime: {jwt_config['REFRESH_TOKEN_LIFETIME']}")
    print(f"Algorithm: {jwt_config['ALGORITHM']}")
    print(f"Rotate Refresh Tokens: {jwt_config.get('ROTATE_REFRESH_TOKENS', False)}")
    print(f"Blacklist After Rotation: {jwt_config.get('BLACKLIST_AFTER_ROTATION', False)}")
    print()


def test_rate_limiting():
    """Test rate limiting configuration"""
    print("=" * 70)
    print("⏱️  RATE LIMITING TEST")
    print("=" * 70)
    print()
    
    print(f"Rate Limit Requests: {config.get_int('RATE_LIMIT_REQUESTS', 100)}")
    print(f"Rate Limit Window: {config.get_int('RATE_LIMIT_WINDOW', 60)} seconds")
    print(f"Login Rate Limit: {config.get_int('LOGIN_RATE_LIMIT', 5)}")
    print(f"Login Rate Window: {config.get_int('LOGIN_RATE_WINDOW', 300)} seconds")
    print()


def test_file_upload():
    """Test file upload configuration"""
    print("=" * 70)
    print("📎 FILE UPLOAD CONFIGURATION TEST")
    print("=" * 70)
    print()
    
    max_size = config.get_int('MAX_UPLOAD_SIZE', 10485760)
    print(f"Max Upload Size: {max_size} bytes ({max_size / 1024 / 1024:.2f} MB)")
    print(f"Allowed Image Extensions: {config.get('ALLOWED_IMAGE_EXTENSIONS', '')}")
    print(f"Allowed Document Extensions: {config.get('ALLOWED_DOCUMENT_EXTENSIONS', '')}")
    print()


def test_logging():
    """Test logging configuration"""
    print("=" * 70)
    print("📝 LOGGING CONFIGURATION TEST")
    print("=" * 70)
    print()
    
    log_config = settings.LOGGING
    print(f"Log Level: {config.get('LOG_LEVEL', 'INFO')}")
    print(f"Log Directory: {config.get('LOG_DIR', 'logs')}")
    print()
    print("Configured Handlers:")
    for handler_name, handler_config in log_config.get('handlers', {}).items():
        print(f"  - {handler_name}: {handler_config.get('class', 'Unknown')}")
    print()


def test_safe_config():
    """Test safe configuration display (with sensitive data masked)"""
    print("=" * 70)
    print("🔐 SAFE CONFIGURATION DISPLAY TEST")
    print("=" * 70)
    print()
    
    safe_config = config.get_safe_config()
    
    print("Environment Variables (sensitive values masked):")
    for key, value in sorted(safe_config.items()):
        if key.startswith('DJANGO') or key.startswith('PYTHON'):
            continue  # Skip system variables
        print(f"  {key}: {value}")
    print()


def main():
    """Run all tests"""
    print()
    print("🚀 DOGGER 2.0 - CONFIGURATION TEST SUITE")
    print()
    
    try:
        test_environment_detection()
        test_database_config()
        test_security_config()
        test_jwt_config()
        test_rate_limiting()
        test_file_upload()
        test_logging()
        test_safe_config()
        
        print("=" * 70)
        print("✅ ALL CONFIGURATION TESTS COMPLETED")
        print("=" * 70)
        print()
        
    except Exception as e:
        print(f"❌ TEST FAILED: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == '__main__':
    main()