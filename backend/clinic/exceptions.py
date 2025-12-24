"""
Dogger 2.0 - Custom Exception Handler
"""
from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status
import logging

logger = logging.getLogger(__name__)


def custom_exception_handler(exc, context):
    """
    Custom exception handler for consistent error responses
    """
    # Call REST framework's default exception handler first
    response = exception_handler(exc, context)
    
    # Log the exception
    logger.error(f"Exception: {exc}", exc_info=True, extra={'context': context})
    
    if response is not None:
        # Standardize error response format
        custom_response_data = {
            'success': False,
            'error': {
                'message': str(exc),
                'details': response.data if isinstance(response.data, dict) else {'detail': response.data},
                'status_code': response.status_code,
            }
        }
        response.data = custom_response_data
    else:
        # Handle unhandled exceptions
        custom_response_data = {
            'success': False,
            'error': {
                'message': 'Internal server error',
                'details': str(exc),
                'status_code': 500,
            }
        }
        response = Response(custom_response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    return response


class SubscriptionLimitExceeded(Exception):
    """Raised when subscription limit is exceeded"""
    pass


class InvalidSharedURL(Exception):
    """Raised when shared URL is invalid or expired"""
    pass


class WhisperAPIError(Exception):
    """Raised when Whisper API fails"""
    pass