#!/usr/bin/env python
"""
Security Audit Script for Dogger 2.0
Performs comprehensive security checks
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv


class SecurityAuditor:
    """Performs security audit checks"""
    
    def __init__(self):
        load_dotenv()
        self.environment = os.getenv('ENVIRONMENT', 'unknown')
        self.passed = []
        self.failed = []
        self.warnings = []
    
    def check_secret_keys(self):
        """Check secret key security"""
        print("🔐 Checking Secret Keys...")
        
        secret_key = os.getenv('SECRET_KEY', '')
        
        # Check if set
        if not secret_key:
            self.failed.append("SECRET_KEY not set")
        else:
            self.passed.append("SECRET_KEY is set")
        
        # Check length
        if len(secret_key) < 50:
            self.failed.append(f"SECRET_KEY too short ({len(secret_key)} chars)")
        else:
            self.passed.append(f"SECRET_KEY length adequate ({len(secret_key)} chars)")
        
        # Check for insecure patterns
        insecure_patterns = ['change-this', 'replace', 'example', 'test', 'default']
        if any(pattern in secret_key.lower() for pattern in insecure_patterns):
            self.failed.append("SECRET_KEY contains insecure placeholder text")
        else:
            self.passed.append("SECRET_KEY contains no obvious placeholders")
        
        # Check complexity
        has_upper = any(c.isupper() for c in secret_key)
        has_lower = any(c.islower() for c in secret_key)
        has_digit = any(c.isdigit() for c in secret_key)
        has_special = any(not c.isalnum() for c in secret_key)
        
        if all([has_upper, has_lower, has_digit, has_special]):
            self.passed.append("SECRET_KEY has good complexity")
        else:
            self.warnings.append("SECRET_KEY complexity could be improved")
    
    def check_debug_mode(self):
        """Check DEBUG setting"""
        print("🐛 Checking DEBUG Mode...")
        
        debug = os.getenv('DEBUG', 'False').lower() == 'true'
        
        if self.environment == 'production' and debug:
            self.failed.append("DEBUG=True in production (CRITICAL SECURITY ISSUE)")
        elif self.environment == 'development' and debug:
            self.passed.append("DEBUG=True in development (OK)")
        elif not debug:
            self.passed.append("DEBUG=False (Secure)")
    
    def check_allowed_hosts(self):
        """Check ALLOWED_HOSTS configuration"""
        print("🌐 Checking ALLOWED_HOSTS...")
        
        # This would need to be read from Django settings
        # For now, just check if environment variable is set
        allowed_hosts = os.getenv('ALLOWED_HOSTS', '')
        
        if not allowed_hosts:
            self.warnings.append("ALLOWED_HOSTS not explicitly set in .env")
        else:
            if '*' in allowed_hosts:
                self.failed.append("ALLOWED_HOSTS contains wildcard (*) - security risk")
            else:
                self.passed.append("ALLOWED_HOSTS properly configured")
    
    def check_database_security(self):
        """Check database security"""
        print("💾 Checking Database Security...")
        
        use_postgres = os.getenv('USE_POSTGRES', 'False').lower() == 'true'
        
        if use_postgres:
            # Check PostgreSQL credentials
            pg_password = os.getenv('PGPASSWORD', '')
            
            weak_passwords = ['postgres', 'password', '123456', 'admin', 'root']
            if pg_password in weak_passwords:
                self.failed.append("PostgreSQL password is weak or default")
            elif len(pg_password) < 12:
                self.warnings.append("PostgreSQL password should be at least 12 characters")
            else:
                self.passed.append("PostgreSQL password appears strong")
            
            # Check SSL mode
            self.passed.append("PostgreSQL configured with SSL")
        else:
            if self.environment == 'production':
                self.warnings.append("Using SQLite in production (consider PostgreSQL)")
            else:
                self.passed.append("SQLite OK for development")
    
    def check_https_settings(self):
        """Check HTTPS/SSL settings"""
        print("🔒 Checking HTTPS/SSL Settings...")
        
        ssl_redirect = os.getenv('SECURE_SSL_REDIRECT', 'False').lower() == 'true'
        session_secure = os.getenv('SESSION_COOKIE_SECURE', 'False').lower() == 'true'
        csrf_secure = os.getenv('CSRF_COOKIE_SECURE', 'False').lower() == 'true'
        
        if self.environment == 'production':
            if not ssl_redirect:
                self.failed.append("SECURE_SSL_REDIRECT=False in production")
            else:
                self.passed.append("SSL redirect enabled")
            
            if not session_secure:
                self.failed.append("SESSION_COOKIE_SECURE=False in production")
            else:
                self.passed.append("Session cookies secured with HTTPS")
            
            if not csrf_secure:
                self.failed.append("CSRF_COOKIE_SECURE=False in production")
            else:
                self.passed.append("CSRF cookies secured with HTTPS")
        else:
            self.passed.append("HTTPS settings appropriate for development")
    
    def check_cors_configuration(self):
        """Check CORS configuration"""
        print("🌍 Checking CORS Configuration...")
        
        cors_origins = os.getenv('CORS_ALLOWED_ORIGINS', '')
        
        if not cors_origins:
            self.warnings.append("CORS_ALLOWED_ORIGINS not set")
            return
        
        # Check for localhost in production
        if self.environment == 'production' and 'localhost' in cors_origins:
            self.failed.append("CORS allows localhost in production")
        
        # Check for wildcard
        if '*' in cors_origins:
            self.failed.append("CORS allows all origins (*) - major security risk")
        
        # Check for http in production
        if self.environment == 'production' and 'http://' in cors_origins:
            self.warnings.append("CORS allows HTTP origins in production")
        
        if len(self.failed) == 0:
            self.passed.append("CORS configuration secure")
    
    def check_rate_limiting(self):
        """Check rate limiting configuration"""
        print("⏱️  Checking Rate Limiting...")
        
        rate_limit = int(os.getenv('RATE_LIMIT_REQUESTS', '0'))
        login_limit = int(os.getenv('LOGIN_RATE_LIMIT', '0'))
        
        if rate_limit == 0:
            self.warnings.append("Rate limiting not configured")
        elif rate_limit > 1000:
            self.warnings.append(f"Rate limit very high ({rate_limit} req/min)")
        else:
            self.passed.append(f"Rate limiting configured ({rate_limit} req/min)")
        
        if login_limit == 0:
            self.warnings.append("Login rate limiting not configured")
        elif login_limit > 10:
            self.warnings.append(f"Login rate limit high ({login_limit} attempts)")
        else:
            self.passed.append(f"Login rate limiting active ({login_limit} attempts)")
    
    def check_jwt_security(self):
        """Check JWT configuration"""
        print("🔑 Checking JWT Security...")
        
        access_lifetime = int(os.getenv('JWT_ACCESS_TOKEN_LIFETIME', '60'))
        
        if access_lifetime > 120:
            self.warnings.append(f"JWT access token lifetime long ({access_lifetime} min)")
        else:
            self.passed.append(f"JWT access token lifetime reasonable ({access_lifetime} min)")
        
        jwt_key = os.getenv('JWT_SIGNING_KEY', '')
        if jwt_key:
            self.passed.append("Separate JWT signing key configured")
        else:
            self.warnings.append("JWT using SECRET_KEY (consider separate key)")
    
    def check_file_upload_security(self):
        """Check file upload security"""
        print("📎 Checking File Upload Security...")
        
        max_size = int(os.getenv('MAX_UPLOAD_SIZE', '0'))
        
        if max_size == 0:
            self.warnings.append("MAX_UPLOAD_SIZE not set")
        elif max_size > 20 * 1024 * 1024:  # 20MB
            self.warnings.append(f"MAX_UPLOAD_SIZE very large ({max_size / 1024 / 1024:.1f}MB)")
        else:
            self.passed.append(f"File upload size limit OK ({max_size / 1024 / 1024:.1f}MB)")
        
        allowed_types = os.getenv('ALLOWED_IMAGE_EXTENSIONS', '')
        if allowed_types:
            dangerous_types = ['.exe', '.bat', '.sh', '.py', '.js']
            if any(ext in allowed_types for ext in dangerous_types):
                self.failed.append("Allowed file types include dangerous extensions")
            else:
                self.passed.append("File type restrictions secure")
    
    def check_logging_configuration(self):
        """Check logging configuration"""
        print("📝 Checking Logging Configuration...")
        
        log_level = os.getenv('LOG_LEVEL', 'INFO')
        log_dir = os.getenv('LOG_DIR', 'logs')
        
        if self.environment == 'production' and log_level == 'DEBUG':
            self.warnings.append("LOG_LEVEL=DEBUG in production (may log sensitive data)")
        else:
            self.passed.append(f"Log level appropriate ({log_level})")
        
        if Path(log_dir).exists():
            self.passed.append(f"Log directory exists ({log_dir})")
        else:
            self.warnings.append(f"Log directory not found ({log_dir})")
    
    def check_sensitive_files(self):
        """Check for sensitive files that shouldn't be committed"""
        print("📁 Checking Sensitive Files...")
        
        sensitive_files = ['.env', 'secrets.txt', '.env.local', 'db.sqlite3']
        gitignore_path = Path('.gitignore')
        
        if gitignore_path.exists():
            with open(gitignore_path, 'r') as f:
                gitignore_content = f.read()
            
            for file in sensitive_files:
                if file in gitignore_content:
                    self.passed.append(f"{file} in .gitignore")
                else:
                    self.failed.append(f"{file} NOT in .gitignore (security risk)")
        else:
            self.failed.append(".gitignore not found")
    
    def run_audit(self):
        """Run complete security audit"""
        print("=" * 70)
        print(f"🔍 SECURITY AUDIT - ENVIRONMENT: {self.environment.upper()}")
        print("=" * 70)
        print()
        
        self.check_secret_keys()
        self.check_debug_mode()
        self.check_allowed_hosts()
        self.check_database_security()
        self.check_https_settings()
        self.check_cors_configuration()
        self.check_rate_limiting()
        self.check_jwt_security()
        self.check_file_upload_security()
        self.check_logging_configuration()
        self.check_sensitive_files()
        
        print()
        print("=" * 70)
        print("📊 AUDIT RESULTS")
        print("=" * 70)
        print()
        
        if self.passed:
            print(f"✅ PASSED ({len(self.passed)}):")
            for item in self.passed:
                print(f"  • {item}")
            print()
        
        if self.warnings:
            print(f"⚠️  WARNINGS ({len(self.warnings)}):")
            for item in self.warnings:
                print(f"  • {item}")
            print()
        
        if self.failed:
            print(f"❌ FAILED ({len(self.failed)}):")
            for item in self.failed:
                print(f"  • {item}")
            print()
        
        # Summary
        total_checks = len(self.passed) + len(self.warnings) + len(self.failed)
        security_score = (len(self.passed) / total_checks * 100) if total_checks > 0 else 0
        
        print("=" * 70)
        print(f"Security Score: {security_score:.1f}% ({len(self.passed)}/{total_checks} checks passed)")
        print("=" * 70)
        print()
        
        if self.failed:
            print("❌ SECURITY AUDIT FAILED")
            print("   Critical issues must be fixed before deployment")
            return False
        elif self.warnings:
            print("⚠️  SECURITY AUDIT PASSED WITH WARNINGS")
            print("   Review warnings before deployment")
            return True
        else:
            print("✅ SECURITY AUDIT PASSED")
            print("   Configuration is secure")
            return True


def main():
    auditor = SecurityAuditor()
    success = auditor.run_audit()
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()