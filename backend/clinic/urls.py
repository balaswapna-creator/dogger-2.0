"""
URL configuration for clinic API
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import views
from .auth_views import (
    SecureTokenObtainPairView,
    logout_view,
    refresh_token_view,
    verify_token,
    user_profile,
    update_profile,
    change_password,
)
from .monitoring import health_check, system_metrics

# Router for ViewSets
router = DefaultRouter()
router.register(r'owners', views.OwnerViewSet, basename='owner')
router.register(r'patients', views.PatientViewSet, basename='patient')
router.register(r'medical-records', views.MedicalRecordViewSet, basename='medicalrecord')
router.register(r'vaccinations', views.VaccinationViewSet, basename='vaccination')
router.register(r'prescriptions', views.PrescriptionViewSet, basename='prescription')
router.register(r'payments', views.PaymentViewSet, basename='payment')
router.register(r'passbooks', views.PassbookViewSet, basename='passbook')
router.register(r'passbooks-public', views.PassbookPublicViewSet, basename='passbook-public')
router.register(r'lab-tests', views.LabTestViewSet, basename='labtest')

urlpatterns = [
    # ========== AUTHENTICATION ENDPOINTS ==========
    
    # Secure login (replaces default TokenObtainPairView)
    path('token/', SecureTokenObtainPairView.as_view(), name='token_obtain_pair'),
    
    # Token refresh
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # Logout (blacklist tokens)
    path('logout/', logout_view, name='logout'),
    
    # Token verification
    path('verify-token/', verify_token, name='verify_token'),
    
    # ========== USER PROFILE ENDPOINTS ==========
    
    # Get current user profile
    path('profile/', user_profile, name='user_profile'),
    
    # Update profile
    path('profile/update/', update_profile, name='update_profile'),
    
    # Change password
    path('profile/change-password/', change_password, name='change_password'),
    
    # ========== DASHBOARD ENDPOINTS ==========
    
    # Dashboard stats
    path('dashboard/stats/', views.dashboard_stats, name='dashboard_stats'),
    
    # Current user
    path('current-user/', views.current_user, name='current_user'),

    # ========== HEALTH & MONITORING ==========
    path('health/', health_check, name='health_check'),
    path('metrics/', system_metrics, name='system_metrics'),
    
    # ========== ROUTER URLS ==========
    
    # Include all ViewSet URLs
    path('', include(router.urls)),

    # Custom passbook public access
    path('passbooks/public/<uuid:access_token>/', 
     views.PassbookPublicViewSet.as_view({'get': 'retrieve'}), 
     name='passbook-public-detail'),

]