"""
Dogger 2.0 - Clinic App Configuration
"""
from django.apps import AppConfig


class ClinicConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'clinic'
    verbose_name = 'Sri Adithya Pet Clinic'
    
    def ready(self):
        """Import signals when app is ready"""
        # Import signals here if needed
        pass