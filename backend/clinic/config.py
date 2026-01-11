"""
Environment Configuration Manager
Handles loading, validation, and secure management of environment variables
"""
import os
import logging
from pathlib import Path
from typing import Any, Dict, Optional
from dotenv import load_dotenv
import secrets

logger = logging.getLogger(__name__)


class ConfigurationError(Exception):
    """Raised when configuration is invalid or missing"""
    pass


class EnvironmentConfig:
    """Manages environment configuration with validation and security"""
    
    # Required environment variables
    REQUIRED_VARS = [
        'SECRET_KEY',
        'ENVIRONMENT',
    ]
    
    # Sensitive variables (should never be logged)
    SENSITIVE_VARS = [
        'SECRET_KEY',
        'JWT_SIGNING_KEY',
        'DATABASE_PASSWORD',
        'EMAIL_HOST_PASSWORD',
        'AWS_SECRET_ACCESS_KEY',
    ]
    
    def __init__(self, env_file: Optional[str] = None):
        """
        Initialize configuration manager
        
        Args:
            env_file: Path to .env file (default: .env in project root)
        """
        self.base_dir = Path(__file__).resolve().parent.parent
        self.env_file = env_file or self.base_dir / '.env'
        self._config: Dict[str, Any] = {}
        self._load_environment()
        self._validate_configuration()
    
    def _load_environment(self):
        """Load environment variables from .env file"""
        if self.env_file.exists():
            load_dotenv(self.env_file)
            logger.info(f"Loaded environment from {self.env_file}")
        else:
            logger.warning(f"No .env file found at {self.env_file}")
    
    def _validate_configuration(self):
        """Validate required configuration variables"""
        missing_vars = []
        
        for var in self.REQUIRED_VARS:
            if not os.getenv(var):
                missing_vars.append(var)
        
        if missing_vars:
            raise ConfigurationError(
                f"Missing required environment variables: {', '.join(missing_vars)}"
            )
        
        # Check for insecure default values in production
        if self.is_production():
            self._validate_production_config()
    
    def _validate_production_config(self):
        """Validate production-specific configuration"""
        issues = []
        
        # Check SECRET_KEY
        secret_key = os.getenv('SECRET_KEY', '')
        if len(secret_key) < 50:
            issues.append("SECRET_KEY must be at least 50 characters in production")
        
        if 'change-this' in secret_key.lower():
            issues.append("SECRET_KEY contains default placeholder value")
        
        # Check DEBUG is False
        if os.getenv('DEBUG', 'False').lower() == 'true':
            issues.append("DEBUG must be False in production")
        
        # Check secure cookie settings
        if os.getenv('SESSION_COOKIE_SECURE', 'False').lower() != 'true':
            issues.append("SESSION_COOKIE_SECURE must be True in production")
        
        if os.getenv('CSRF_COOKIE_SECURE', 'False').lower() != 'true':
            issues.append("CSRF_COOKIE_SECURE must be True in production")
        
        if issues:
            error_msg = "Production configuration issues:\n" + "\n".join(f"- {issue}" for issue in issues)
            raise ConfigurationError(error_msg)
    
    def get(self, key: str, default: Any = None, required: bool = False) -> Any:
        """
        Get configuration value
        
        Args:
            key: Configuration key
            default: Default value if not found
            required: Raise error if not found
        
        Returns:
            Configuration value
        """
        value = os.getenv(key, default)
        
        if required and value is None:
            raise ConfigurationError(f"Required configuration '{key}' not found")
        
        return value
    
    def get_bool(self, key: str, default: bool = False) -> bool:
        """Get boolean configuration value"""
        value = self.get(key, str(default))
        return value.lower() in ('true', '1', 'yes', 'on')
    
    def get_int(self, key: str, default: int = 0) -> int:
        """Get integer configuration value"""
        value = self.get(key, str(default))
        try:
            return int(value)
        except (ValueError, TypeError):
            return default
    
    def get_list(self, key: str, default: Optional[list] = None, separator: str = ',') -> list:
        """Get list configuration value"""
        value = self.get(key, '')
        if not value:
            return default or []
        return [item.strip() for item in value.split(separator)]
    
    def is_production(self) -> bool:
        """Check if running in production environment"""
        return self.get('ENVIRONMENT', 'development').lower() == 'production'
    
    def is_development(self) -> bool:
        """Check if running in development environment"""
        return self.get('ENVIRONMENT', 'development').lower() == 'development'
    
    def is_staging(self) -> bool:
        """Check if running in staging environment"""
        return self.get('ENVIRONMENT', 'development').lower() == 'staging'
    
    def get_safe_config(self) -> Dict[str, Any]:
        """
        Get configuration dictionary with sensitive values masked
        Useful for logging and debugging
        """
        safe_config = {}
        
        for key, value in os.environ.items():
            if any(sensitive in key.upper() for sensitive in self.SENSITIVE_VARS):
                safe_config[key] = '***REDACTED***'
            else:
                safe_config[key] = value
        
        return safe_config
    
    def validate_secret_strength(self, secret: str, min_length: int = 50) -> bool:
        """
        Validate that a secret meets security requirements
        
        Args:
            secret: Secret to validate
            min_length: Minimum required length
        
        Returns:
            True if secret is strong enough
        """
        if len(secret) < min_length:
            return False
        
        # Check for variety of characters
        has_upper = any(c.isupper() for c in secret)
        has_lower = any(c.islower() for c in secret)
        has_digit = any(c.isdigit() for c in secret)
        has_special = any(not c.isalnum() for c in secret)
        
        return has_upper and has_lower and has_digit and has_special


class SecretKeyManager:
    """Manages secret key generation and rotation"""
    
    @staticmethod
    def generate_secret_key(length: int = 50) -> str:
        """
        Generate a secure random secret key
        
        Args:
            length: Length of the secret key
        
        Returns:
            Secure random string
        """
        return secrets.token_urlsafe(length)
    
    @staticmethod
    def generate_django_secret_key() -> str:
        """Generate a Django-compatible secret key"""
        chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
        return ''.join(secrets.choice(chars) for _ in range(50))
    
    @staticmethod
    def rotate_secret_key(old_key: str) -> str:
        """
        Rotate secret key (generate new one)
        
        Args:
            old_key: Current secret key (for logging/audit)
        
        Returns:
            New secret key
        """
        logger.info("Rotating secret key...")
        new_key = SecretKeyManager.generate_django_secret_key()
        logger.info("Secret key rotated successfully")
        return new_key


# Global configuration instance
config = EnvironmentConfig()


# Convenience functions
def get_config(key: str, default: Any = None) -> Any:
    """Get configuration value"""
    return config.get(key, default)


def is_production() -> bool:
    """Check if running in production"""
    return config.is_production()


def is_development() -> bool:
    """Check if running in development"""
    return config.is_development()


def get_safe_config() -> Dict[str, Any]:
    """Get safe configuration for logging"""
    return config.get_safe_config()