"""
Dogger 2.0 - View Mixins
"""
from rest_framework.response import Response
from rest_framework import status
from .models import AuditLog
import logging

logger = logging.getLogger(__name__)


class AuditLogMixin:
    """Mixin to add audit logging to views"""
    
    def log_action(self, action, model_name, object_id, description=''):
        """Create audit log entry"""
        try:
            ip_address = self.get_client_ip()
            user_agent = self.request.META.get('HTTP_USER_AGENT', '')
            
            AuditLog.objects.create(
                user=self.request.user if self.request.user.is_authenticated else None,
                action=action,
                model_name=model_name,
                object_id=object_id,
                description=description,
                ip_address=ip_address,
                user_agent=user_agent
            )
        except Exception as e:
            logger.error(f"Failed to create audit log: {e}")
    
    def get_client_ip(self):
        """Get client IP address"""
        x_forwarded_for = self.request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = self.request.META.get('REMOTE_ADDR')
        return ip


class SubscriptionCheckMixin:
    """Mixin to check subscription limits"""
    
    def check_subscription_limit(self, feature_type):
        """
        Check if user has reached subscription limit
        feature_type: 'pdf_export' or 'voice_transcription'
        """
        user = self.request.user
        
        if user.is_staff:
            return True
        
        try:
            subscription = user.subscription
            
            if not subscription.is_active:
                return False
            
            # Check monthly limits
            from django.utils import timezone
            from datetime import timedelta
            
            # Reset monthly counters if needed
            if subscription.last_reset < timezone.now() - timedelta(days=30):
                subscription.reset_monthly_limits()
            
            if feature_type == 'pdf_export':
                if subscription.current_pdf_exports >= subscription.pdf_exports_limit:
                    return False
                subscription.current_pdf_exports += 1
                subscription.save()
            
            elif feature_type == 'voice_transcription':
                if subscription.current_voice_uses >= subscription.voice_transcriptions_limit:
                    return False
                subscription.current_voice_uses += 1
                subscription.save()
            
            return True
            
        except Exception as e:
            logger.error(f"Subscription check failed: {e}")
            return False


class SuccessResponseMixin:
    """Mixin for consistent success responses"""
    
    def success_response(self, data=None, message='Success', status_code=status.HTTP_200_OK):
        """Return standardized success response"""
        response_data = {
            'success': True,
            'message': message,
            'data': data
        }
        return Response(response_data, status=status_code)
    
    def error_response(self, message='Error', errors=None, status_code=status.HTTP_400_BAD_REQUEST):
        """Return standardized error response"""
        response_data = {
            'success': False,
            'message': message,
            'errors': errors
        }
        return Response(response_data, status=status_code)