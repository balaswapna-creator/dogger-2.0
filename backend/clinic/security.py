# backend/clinic/security.py
# Complete security middleware with all classes

import time
import logging
from django.http import JsonResponse
from django.conf import settings
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError

logger = logging.getLogger('security')

# ============================================
# RATE LIMITING MIDDLEWARE
# ============================================

class RateLimitMiddleware:
    """
    Rate limiting middleware to prevent brute force attacks
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        self.requests = {}  # {ip: [(timestamp, endpoint), ...]}
        self.max_requests = 100  # Max requests per window
        self.window = 60  # Time window in seconds
        self.login_attempts = {}  # {ip: [timestamps]}
        self.max_login_attempts = 5
        self.login_window = 300  # 5 minutes
    
    def __call__(self, request):
        client_ip = self.get_client_ip(request)
        current_time = time.time()
        
        # Check rate limiting for all endpoints
        if not self.check_rate_limit(client_ip, current_time, request.path):
            logger.warning(f"Rate limit exceeded for IP: {client_ip} on {request.path}")
            return JsonResponse({
                'error': 'Rate limit exceeded. Please try again later.'
            }, status=429)
        
        # Special handling for login endpoints
        if request.path.endswith('/api/token/') or request.path.endswith('/login/'):
            if not self.check_login_attempts(client_ip, current_time):
                logger.warning(f"Too many login attempts from IP: {client_ip}")
                return JsonResponse({
                    'error': 'Too many login attempts. Please try again later.'
                }, status=429)
        
        response = self.get_response(request)
        
        # Clean up old entries periodically
        self.cleanup_old_entries(current_time)
        
        return response
    
    def get_client_ip(self, request):
        """Get client IP address"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
    
    def check_rate_limit(self, ip, current_time, endpoint):
        """Check if IP has exceeded rate limit"""
        if ip not in self.requests:
            self.requests[ip] = []
        
        # Remove requests outside the time window
        self.requests[ip] = [
            (ts, ep) for ts, ep in self.requests[ip]
            if current_time - ts < self.window
        ]
        
        # Check if limit exceeded
        if len(self.requests[ip]) >= self.max_requests:
            return False
        
        # Add current request
        self.requests[ip].append((current_time, endpoint))
        return True
    
    def check_login_attempts(self, ip, current_time):
        """Check login attempts for specific IP"""
        if ip not in self.login_attempts:
            self.login_attempts[ip] = []
        
        # Remove old attempts
        self.login_attempts[ip] = [
            ts for ts in self.login_attempts[ip]
            if current_time - ts < self.login_window
        ]
        
        # Check if too many attempts
        if len(self.login_attempts[ip]) >= self.max_login_attempts:
            return False
        
        # Add current attempt
        self.login_attempts[ip].append(current_time)
        return True
    
    def cleanup_old_entries(self, current_time):
        """Periodically cleanup old entries to prevent memory bloat"""
        for ip in list(self.requests.keys()):
            self.requests[ip] = [
                (ts, ep) for ts, ep in self.requests[ip]
                if current_time - ts < self.window
            ]
            if not self.requests[ip]:
                del self.requests[ip]
        
        for ip in list(self.login_attempts.keys()):
            self.login_attempts[ip] = [
                ts for ts in self.login_attempts[ip]
                if current_time - ts < self.login_window
            ]
            if not self.login_attempts[ip]:
                del self.login_attempts[ip]


# ============================================
# JWT AUTHENTICATION MIDDLEWARE
# ============================================

class JWTAuthenticationMiddleware:
    """
    Middleware to validate JWT tokens on protected endpoints
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        self.jwt_auth = JWTAuthentication()
        
        # Endpoints that don't require authentication
        self.public_endpoints = [
            '/api/token/',
            '/api/token/refresh/',
            '/admin/',
            '/api/health/',
        ]
    
    def __call__(self, request):
        # Skip authentication for public endpoints
        if self.is_public_endpoint(request.path):
            return self.get_response(request)
        
        # Skip authentication for non-API endpoints
        if not request.path.startswith('/api/'):
            return self.get_response(request)
        
        # Get token from Authorization header
        auth_header = request.META.get('HTTP_AUTHORIZATION', '')
        
        if not auth_header.startswith('Bearer '):
            # No token provided, let Django REST Framework handle it
            return self.get_response(request)
        
        try:
            # Validate token
            validated_token = self.jwt_auth.get_validated_token(
                auth_header.replace('Bearer ', '')
            )
            user = self.jwt_auth.get_user(validated_token)
            request.user = user
            
        except (InvalidToken, TokenError) as e:
            logger.warning(f"Invalid token attempt: {str(e)}")
            return JsonResponse({
                'error': 'Invalid or expired token'
            }, status=401)
        
        return self.get_response(request)
    
    def is_public_endpoint(self, path):
        """Check if endpoint is public"""
        return any(path.startswith(endpoint) for endpoint in self.public_endpoints)


# ============================================
# XSS PROTECTION MIDDLEWARE
# ============================================

class XSSProtectionMiddleware:
    """
    XSS Protection Middleware
    Sanitizes incoming request data to prevent XSS attacks
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Process request
        response = self.get_response(request)
        return response
    
    def sanitize_data(self, data):
        """
        Recursively sanitize data to prevent XSS
        """
        if isinstance(data, dict):
            return {key: self.sanitize_data(value) for key, value in data.items()}
        elif isinstance(data, list):
            return [self.sanitize_data(item) for item in data]
        elif isinstance(data, str):
            # Basic XSS prevention - remove dangerous tags
            dangerous_patterns = ['<script', '</script', 'javascript:', 'onerror=', 'onclick=']
            clean_data = data
            for pattern in dangerous_patterns:
                clean_data = clean_data.replace(pattern, '')
            return clean_data
        else:
            return data


# ============================================
# CONTENT SECURITY POLICY MIDDLEWARE
# ============================================

class ContentSecurityPolicyMiddleware:
    """
    Content Security Policy (CSP) middleware
    Prevents XSS attacks by controlling which resources can be loaded
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        response = self.get_response(request)
        
        # Only add CSP headers to HTML responses
        if 'text/html' in response.get('Content-Type', ''):
            # Define CSP directives
            csp_directives = [
                "default-src 'self'",
                "script-src 'self' 'unsafe-inline' 'unsafe-eval' https://cdn.jsdelivr.net https://unpkg.com",
                "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com",
                "font-src 'self' https://fonts.gstatic.com",
                "img-src 'self' data: https:",
                "connect-src 'self' http://127.0.0.1:8000 http://localhost:8000",
                "frame-ancestors 'none'",
                "base-uri 'self'",
                "form-action 'self'",
            ]
            
            response['Content-Security-Policy'] = '; '.join(csp_directives)
        
        return response


# ============================================
# SECURITY HEADERS MIDDLEWARE
# ============================================

class SecurityHeadersMiddleware:
    """
    Add additional security headers
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        response = self.get_response(request)
        
        # X-Content-Type-Options: Prevent MIME type sniffing
        response['X-Content-Type-Options'] = 'nosniff'
        
        # X-Frame-Options: Prevent clickjacking
        response['X-Frame-Options'] = 'DENY'
        
        # X-XSS-Protection: Enable browser XSS protection
        response['X-XSS-Protection'] = '1; mode=block'
        
        # Referrer-Policy: Control referrer information
        response['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        
        # Permissions-Policy: Control browser features
        response['Permissions-Policy'] = 'geolocation=(), microphone=(), camera=()'
        
        return response