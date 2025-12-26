"""
Dogger 2.0 URL Configuration
"""
from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

def api_root(request):
    """Root endpoint - shows API is working"""
    return JsonResponse({
        'message': 'Dogger 2.0 API is running!',
        'endpoints': {
            'admin': '/admin/',
            'api': '/api/',
            'patients': '/api/patients/',
            'owners': '/api/owners/',
            'vaccinations': '/api/vaccinations/',
            'medical_records': '/api/medical-records/',
            'payments': '/api/payments/',
            'prescriptions': '/api/prescriptions/',
            'passbooks': '/api/passbooks/',
        }
    })

urlpatterns = [
      path('', api_root, name='api-root'),
      path('admin/', admin.site.urls),
      path('api/', include('clinic.urls')),
    
    # JWT Authentication
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
       
    # ALL CLINIC ROUTES (including passbooks)
    path('api/', include('clinic.urls')),
]

# Serve media files in development
if settings.DEBUG: 
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    