#!/usr/bin/env python
"""
Environment Configuration Validator
Validates environment configuration before deployment
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv


class ConfigValidator:
    """Validates environment configuration"""
    
    def __init__(self, env_file='.env'):
        self.env_file = Path(env_file)
        self.errors = []
        self.warnings = []
        
        if not self.env_file.exists():
            print(f"❌ Environment file not found: {env_file}")
            sys.exit(1)
        
        load_dotenv(self.env_file)
        self.environment = os.getenv('ENVIRONMENT', 'unknown')
    
    def validate_secret_key(self):
        """Validate SECRET_KEY"""
        secret_key = os.getenv('SECRET_KEY', '')
        
        if not secret_key:
            self.errors.append("SECRET_KEY is not set")
            return
        
        if len(secret_key) < 50:
            self.errors.append(f"SECRET_KEY too short ({len(secret_key)} chars, minimum 50)")
        
        if 'change-this' in secret_key.lower() or 'replace' in secret_key.lower():
            self.errors.append("SECRET_KEY contains placeholder text")
        
        if 'insecure' in secret_key.lower() and self.environment != 'development':
            self.errors.append("SECRET_KEY contains 'insecure' flag in non-development environment")
    
    def validate_database(self):
        """Validate database configuration"""
        use_postgres = os.getenv('USE_POSTGRES', 'False').lower() == 'true'
        
        if use_postgres:
            required = ['PGDATABASE', 'PGUSER', 'PGPASSWORD', 'PGHOST']
            for key in required:
                if not os.getenv(key):
                    self.errors.append(f"PostgreSQL is enabled but {key} is not set")
            
            # Check for default passwords
            pg_password = os.getenv('PGPASSWORD', '')
            if pg_password in ['postgres', 'password', '123456', 'admin']:
                self.errors.append("PostgreSQL password is too weak or default")
    
    def validate_security_settings(self):
        """Validate security settings"""
        is_production = self.environment == 'production'
        
        # Check DEBUG mode
        debug = os.getenv('DEBUG', 'False').lower() == 'true'
        if debug and is_production:
            self.errors.append("DEBUG is True in production environment")
        
        # Check cookie security
        if is_production:
            if os.getenv('SESSION_COOKIE_SECURE', 'False').lower() != 'true':
                self.errors.append("SESSION_COOKIE_SECURE must be True in production")
            
            if os.getenv('CSRF_COOKIE_SECURE', 'False').lower() != 'true':
                self.errors.append("CSRF_COOKIE_SECURE must be True in production")
            
            if os.getenv('SECURE_SSL_REDIRECT', 'False').lower() != 'true':
                self.warnings.append("SECURE_SSL_REDIRECT should be True in production")
    
    def validate_jwt_settings(self):
        """Validate JWT settings"""
        jwt_key = os.getenv('JWT_SIGNING_KEY', '')
        
        if not jwt_key:
            self.warnings.append("JWT_SIGNING_KEY not set (using SECRET_KEY)")
        elif 'replace' in jwt_key.lower():
            self.errors.append("JWT_SIGNING_KEY contains placeholder text")
        
        # Check token lifetime
        access_lifetime = int(os.getenv('JWT_ACCESS_TOKEN_LIFETIME', '60'))
        if access_lifetime > 120 and self.environment == 'production':
            self.warnings.append(f"JWT access token lifetime is high ({access_lifetime} min) for production")
    
    def validate_cors_settings(self):
        """Validate CORS settings"""
        cors_origins = os.getenv('CORS_ALLOWED_ORIGINS', '')
        
        if not cors_origins:
            self.warnings.append("CORS_ALLOWED_ORIGINS is empty")
            return
        
        # Check for localhost in production
        if self.environment == 'production' and 'localhost' in cors_origins:
            self.errors.append("CORS_ALLOWED_ORIGINS contains localhost in production")
        
        # Check for http:// in production
        if self.environment == 'production' and 'http://' in cors_origins:
            self.warnings.append("CORS_ALLOWED_ORIGINS contains http:// URLs in production (should be https://)")
    
    def validate_email_settings(self):
        """Validate email settings"""
        email_backend = os.getenv('EMAIL_BACKEND', '')
        
        if 'console' in email_backend and self.environment == 'production':
            self.errors.append("Email backend is set to console in production")
        
        if 'smtp' in email_backend:
            required = ['EMAIL_HOST', 'EMAIL_PORT', 'EMAIL_HOST_USER', 'EMAIL_HOST_PASSWORD']
            for key in required:
                if not os.getenv(key):
                    self.warnings.append(f"SMTP is configured but {key} is not set")
    
    def validate_file_upload(self):
        """Validate file upload settings"""
        max_size = int(os.getenv('MAX_UPLOAD_SIZE', '0'))
        
        if max_size == 0:
            self.warnings.append("MAX_UPLOAD_SIZE is not set")
        elif max_size > 10 * 1024 * 1024:  # 10MB
            self.warnings.append(f"MAX_UPLOAD_SIZE is large ({max_size / 1024 / 1024:.1f}MB)")
    
    def validate_cloudinary(self):
        """Validate Cloudinary settings"""
        if self.environment in ['staging', 'production']:
            required = ['CLOUDINARY_CLOUD_NAME', 'CLOUDINARY_API_KEY', 'CLOUDINARY_API_SECRET']
            missing = [key for key in required if not os.getenv(key)]
            
            if missing:
                self.warnings.append(f"Cloudinary not fully configured: {', '.join(missing)}")
    
    def validate_all(self):
        """Run all validations"""
        print("=" * 70)
        print(f"🔍 VALIDATING ENVIRONMENT: {self.environment.upper()}")
        print("=" * 70)
        print()
        
        self.validate_secret_key()
        self.validate_database()
        self.validate_security_settings()
        self.validate_jwt_settings()
        self.validate_cors_settings()
        self.validate_email_settings()
        self.validate_file_upload()
        self.validate_cloudinary()
        
        # Print results
        if self.errors:
            print("❌ ERRORS:")
            for error in self.errors:
                print(f"  • {error}")
            print()
        
        if self.warnings:
            print("⚠️  WARNINGS:")
            for warning in self.warnings:
                print(f"  • {warning}")
            print()
        
        if not self.errors and not self.warnings:
            print("✅ All validations passed!")
            print()
        
        # Summary
        print("=" * 70)
        print(f"Errors: {len(self.errors)}, Warnings: {len(self.warnings)}")
        print("=" * 70)
        print()
        
        if self.errors:
            print("❌ Configuration validation FAILED")
            print("   Fix the errors above before deploying")
            sys.exit(1)
        else:
            print("✅ Configuration validation PASSED")
            if self.warnings:
                print("   Review warnings before deploying")
            sys.exit(0)


def main():
    env_file = sys.argv[1] if len(sys.argv) > 1 else '.env'
    validator = ConfigValidator(env_file)
    validator.validate_all()


if __name__ == '__main__':
    main()