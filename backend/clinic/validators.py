# Create: backend/clinic/validators.py

import re
from django.core.exceptions import ValidationError
from django.core.validators import validate_email as django_validate_email
import bleach

class InputValidator:
    """Server-side input validation and sanitization"""
    
    # Allowed HTML tags for rich text (if needed)
    ALLOWED_TAGS = ['p', 'br', 'strong', 'em', 'u', 'ol', 'ul', 'li']
    ALLOWED_ATTRIBUTES = {}
    
    @staticmethod
    def sanitize_html(value):
        """
        Sanitize HTML input to prevent XSS
        """
        if not value:
            return value
        
        # Use bleach to clean HTML
        return bleach.clean(
            value,
            tags=InputValidator.ALLOWED_TAGS,
            attributes=InputValidator.ALLOWED_ATTRIBUTES,
            strip=True
        )
    
    @staticmethod
    def sanitize_input(value):
        """
        Basic input sanitization - remove dangerous characters
        """
        if not value:
            return value
        
        # Remove null bytes
        value = value.replace('\x00', '')
        
        # Remove control characters except newline and tab
        value = ''.join(char for char in value if ord(char) >= 32 or char in '\n\t')
        
        # Strip leading/trailing whitespace
        value = value.strip()
        
        return value
    
    @staticmethod
    def validate_email(email):
        """
        Validate email format
        """
        if not email:
            raise ValidationError("Email is required")
        
        try:
            django_validate_email(email)
        except ValidationError:
            raise ValidationError("Invalid email format")
        
        return email.lower().strip()
    
    @staticmethod
    def validate_phone(phone):
        """
        Validate phone number format (basic international)
        """
        if not phone:
            raise ValidationError("Phone number is required")
        
        # Remove spaces, dashes, parentheses
        clean_phone = re.sub(r'[\s\-\(\)]', '', phone)
        
        # Check if it's a valid phone number (10+ digits, optional +)
        if not re.match(r'^\+?\d{10,}$', clean_phone):
            raise ValidationError("Invalid phone number format")
        
        return clean_phone
    
    @staticmethod
    def validate_password_strength(password):
        """
        Validate password meets security requirements
        Returns list of errors if invalid
        """
        errors = []
        
        if len(password) < 8:
            errors.append("Password must be at least 8 characters long")
        
        if not re.search(r'[A-Z]', password):
            errors.append("Password must contain at least one uppercase letter")
        
        if not re.search(r'[a-z]', password):
            errors.append("Password must contain at least one lowercase letter")
        
        if not re.search(r'\d', password):
            errors.append("Password must contain at least one number")
        
        if not re.search(r'[!@#$%^&*()_+\-=\[\]{};:\'",.<>?]', password):
            errors.append("Password must contain at least one special character")
        
        if errors:
            raise ValidationError(errors)
        
        return True
    
    @staticmethod
    def validate_username(username):
        """
        Validate username format
        """
        if not username:
            raise ValidationError("Username is required")
        
        # 3-20 characters, alphanumeric and underscore only
        if not re.match(r'^[a-zA-Z0-9_]{3,20}$', username):
            raise ValidationError(
                "Username must be 3-20 characters and contain only letters, numbers, and underscores"
            )
        
        return username.lower().strip()
    
    @staticmethod
    def validate_date_format(date_string):
        """
        Validate date string format (YYYY-MM-DD)
        """
        if not date_string:
            raise ValidationError("Date is required")
        
        if not re.match(r'^\d{4}-\d{2}-\d{2}$', date_string):
            raise ValidationError("Date must be in YYYY-MM-DD format")
        
        return date_string
    
    @staticmethod
    def validate_numeric_range(value, min_val, max_val, field_name="Value"):
        """
        Validate numeric value is within range
        """
        try:
            num = float(value)
        except (TypeError, ValueError):
            raise ValidationError(f"{field_name} must be a valid number")
        
        if num < min_val or num > max_val:
            raise ValidationError(
                f"{field_name} must be between {min_val} and {max_val}"
            )
        
        return num
    
    @staticmethod
    def validate_no_sql_injection(value):
        """
        Check for common SQL injection patterns
        """
        if not value:
            return value
        
        # Common SQL injection patterns
        dangerous_patterns = [
            r"(\bOR\b.*=.*)",
            r"(\bAND\b.*=.*)",
            r"(--)",
            r"(/\*|\*/)",
            r"(\bUNION\b)",
            r"(\bSELECT\b)",
            r"(\bINSERT\b)",
            r"(\bUPDATE\b)",
            r"(\bDELETE\b)",
            r"(\bDROP\b)",
            r"(;)",
            r"(\bEXEC\b)",
        ]
        
        value_upper = value.upper()
        for pattern in dangerous_patterns:
            if re.search(pattern, value_upper):
                raise ValidationError("Input contains potentially dangerous characters")
        
        return value


class FileValidator:
    """File upload validation"""
    
    ALLOWED_IMAGE_EXTENSIONS = ['jpg', 'jpeg', 'png', 'gif', 'webp']
    ALLOWED_DOCUMENT_EXTENSIONS = ['pdf', 'doc', 'docx', 'txt']
    
    MAX_IMAGE_SIZE = 5 * 1024 * 1024  # 5MB
    MAX_DOCUMENT_SIZE = 10 * 1024 * 1024  # 10MB
    
    @staticmethod
    def validate_file_extension(filename, allowed_extensions):
        """
        Validate file extension
        """
        ext = filename.rsplit('.', 1)[-1].lower() if '.' in filename else ''
        
        if ext not in allowed_extensions:
            raise ValidationError(
                f"File type not allowed. Allowed types: {', '.join(allowed_extensions)}"
            )
        
        return ext
    
    @staticmethod
    def validate_file_size(file_size, max_size):
        """
        Validate file size
        """
        if file_size > max_size:
            max_mb = max_size / (1024 * 1024)
            raise ValidationError(f"File size exceeds maximum of {max_mb}MB")
        
        return True
    
    @staticmethod
    def sanitize_filename(filename):
        """
        Sanitize filename to prevent path traversal
        """
        # Remove path separators
        filename = filename.replace('/', '_').replace('\\', '_')
        
        # Remove null bytes
        filename = filename.replace('\x00', '')
        
        # Remove dangerous characters
        filename = re.sub(r'[^\w\s\-\.]', '_', filename)
        
        # Remove leading/trailing dots and spaces
        filename = filename.strip('. ')
        
        return filename
    
    @staticmethod
    def validate_image_file(uploaded_file):
        """
        Validate uploaded image file
        """
        # Validate extension
        ext = FileValidator.validate_file_extension(
            uploaded_file.name,
            FileValidator.ALLOWED_IMAGE_EXTENSIONS
        )
        
        # Validate size
        FileValidator.validate_file_size(
            uploaded_file.size,
            FileValidator.MAX_IMAGE_SIZE
        )
        
        # Sanitize filename
        safe_name = FileValidator.sanitize_filename(uploaded_file.name)
        
        return safe_name
    
    @staticmethod
    def validate_document_file(uploaded_file):
        """
        Validate uploaded document file
        """
        # Validate extension
        ext = FileValidator.validate_file_extension(
            uploaded_file.name,
            FileValidator.ALLOWED_DOCUMENT_EXTENSIONS
        )
        
        # Validate size
        FileValidator.validate_file_size(
            uploaded_file.size,
            FileValidator.MAX_DOCUMENT_SIZE
        )
        
        # Sanitize filename
        safe_name = FileValidator.sanitize_filename(uploaded_file.name)
        
        return safe_name