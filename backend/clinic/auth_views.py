"""
Enhanced authentication views with security features
"""

from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, throttle_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import authenticate
from django.utils import timezone
from django.core.cache import cache
import hashlib
import logging

logger = logging.getLogger('security')


def get_client_ip(request):
    """Helper function to get client IP"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


# ============================================================================
# SECURE LOGIN VIEW - NO THROTTLING FOR NOW
# ============================================================================

class SecureTokenObtainPairView(TokenObtainPairView):
    """
    Enhanced login view with security logging
    TEMPORARILY DISABLED THROTTLING for testing
    """
    throttle_classes = []  # Disable throttling temporarily
    
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        ip = self.get_client_ip(request)
        
        # Authenticate user
        user = authenticate(username=username, password=password)
        
        if user:
            # Log successful login
            logger.info(f'Login success: {username} from {ip}')
            
            # Update last login
            user.last_login = timezone.now()
            user.save(update_fields=['last_login'])
            
            # Generate tokens
            response = super().post(request, *args, **kwargs)
            
            # Add security headers
            response['X-Content-Type-Options'] = 'nosniff'
            response['X-Frame-Options'] = 'DENY'
            
            return response
        else:
            # Log failed login
            logger.warning(f'Login failed: {username or "unknown"} from {ip}')
            
            return Response({
                'error': 'Invalid credentials',
                'code': 'invalid_credentials'
            }, status=status.HTTP_401_UNAUTHORIZED)
    
    def get_client_ip(self, request):
        """Get client IP address"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip


# ============================================================================
# LOGOUT VIEW
# ============================================================================

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    """
    Secure logout - blacklist refresh token
    """
    try:
        # Get refresh token from request
        refresh_token = request.data.get('refresh_token')
        
        if refresh_token:
            # Blacklist the refresh token in cache
            token_hash = hashlib.sha256(refresh_token.encode()).hexdigest()
            cache.set(f'blacklist_{token_hash}', True, 7*24*60*60)  # 7 days
            
            # Also blacklist the access token
            auth_header = request.META.get('HTTP_AUTHORIZATION', '')
            if auth_header.startswith('Bearer '):
                access_token = auth_header.split(' ')[1]
                access_hash = hashlib.sha256(access_token.encode()).hexdigest()
                cache.set(f'blacklist_{access_hash}', True, 3600)  # 1 hour
        
        # Log logout
        ip = get_client_ip(request)
        logger.info(f'Logout: {request.user.username} from {ip}')
        
        return Response({
            'message': 'Logged out successfully'
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        logger.error(f'Logout error: {str(e)}')
        return Response({
            'error': 'Logout failed',
            'code': 'logout_error'
        }, status=status.HTTP_400_BAD_REQUEST)


# ============================================================================
# TOKEN REFRESH VIEW
# ============================================================================

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def refresh_token_view(request):
    """
    Refresh access token with security checks
    """
    try:
        refresh_token = request.data.get('refresh')
        
        if not refresh_token:
            return Response({
                'error': 'Refresh token required',
                'code': 'missing_token'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Check if token is blacklisted
        token_hash = hashlib.sha256(refresh_token.encode()).hexdigest()
        if cache.get(f'blacklist_{token_hash}'):
            return Response({
                'error': 'Token has been revoked',
                'code': 'token_revoked'
            }, status=status.HTTP_401_UNAUTHORIZED)
        
        # Generate new access token
        token = RefreshToken(refresh_token)
        access_token = str(token.access_token)
        
        # Log token refresh
        logger.info(f'Token refreshed for user: {request.user.username}')
        
        return Response({
            'access': access_token
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        logger.error(f'Token refresh error: {str(e)}')
        return Response({
            'error': 'Invalid refresh token',
            'code': 'invalid_token'
        }, status=status.HTTP_401_UNAUTHORIZED)


# ============================================================================
# TOKEN VERIFICATION
# ============================================================================
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def verify_token(request):
    """
    Verify if current token is valid
    """
    user = request.user
    return Response({
        'valid': True,
        'user': {
            'id': str(user.id),
            'username': user.username,
            'role': getattr(user, 'role', 'staff'),
            'email': getattr(user, 'email', ''),
        }
    }, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_profile(request):
    """
    Get current user profile
    """
    user = request.user
    
    return Response({
        'id': str(user.id),
        'username': user.username,
        'email': getattr(user, 'email', ''),
        'first_name': getattr(user, 'first_name', ''),
        'last_name': getattr(user, 'last_name', ''),
        'role': getattr(user, 'role', 'staff'),
        'last_login': user.last_login,
    }, status=status.HTTP_200_OK)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_profile(request):
    """
    Update current user profile
    """
    user = request.user
    
    # Update allowed fields
    allowed_fields = ['email', 'first_name', 'last_name']
    
    for field in allowed_fields:
        if field in request.data:
            setattr(user, field, request.data[field])
    
    user.save()
    
    # Log profile update
    ip = get_client_ip(request)
    logger.info(f'Profile updated: {user.username} from {ip}')
    
    return Response({
        'message': 'Profile updated successfully',
        'user': {
            'id': str(user.id),
            'username': user.username,
            'email': getattr(user, 'email', ''),
            'first_name': getattr(user, 'first_name', ''),
            'last_name': getattr(user, 'last_name', ''),
            'role': getattr(user, 'role', 'staff'),
        }
    }, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def change_password(request):
    """
    Change user password
    """
    current_password = request.data.get('current_password')
    new_password = request.data.get('new_password')
    
    if not current_password or not new_password:
        return Response({
            'error': 'Current and new password required',
            'code': 'missing_data'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    user = request.user
    
    # Verify current password
    if not user.check_password(current_password):
        return Response({
            'error': 'Current password is incorrect',
            'code': 'invalid_password'
        }, status=status.HTTP_400_BAD_REQUEST)
    
    # Set new password
    user.set_password(new_password)
    user.save()
    
    # Log password change
    ip = get_client_ip(request)
    logger.info(f'Password changed: {user.username} from {ip}')
    
    return Response({
        'message': 'Password changed successfully'
    }, status=status.HTTP_200_OK)