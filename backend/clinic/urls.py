# ============================================
# FILE: backend/clinic/urls.py
# COMPLETE URL CONFIGURATION
# ============================================

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from .views import (
    PatientViewSet,
    OwnerViewSet,
    MedicalRecordViewSet,
    PaymentViewSet,
    VaccinationViewSet,
    PrescriptionViewSet,
    PassbookViewSet,
    PassbookPublicViewSet
)

# Create router for standard ViewSets
router = DefaultRouter()
router.register(r'patients', PatientViewSet, basename='patient')
router.register(r'owners', OwnerViewSet, basename='owner')
router.register(r'medical-records', MedicalRecordViewSet, basename='medicalrecord')
router.register(r'payments', PaymentViewSet, basename='payment')
router.register(r'vaccinations', VaccinationViewSet, basename='vaccination')
router.register(r'prescriptions', PrescriptionViewSet, basename='prescription')
router.register(r'passbooks', PassbookViewSet, basename='passbook')

urlpatterns = [
    # Include all router URLs
    path('', include(router.urls)),
    path('auth/me/', views.current_user, name='current-user'),
    
    # PUBLIC PASSBOOK ACCESS (no authentication required)
    # This MUST be outside the router to work properly
    path('passbook/<uuid:token>/', 
         PassbookPublicViewSet.as_view({'get': 'retrieve'}), 
         name='passbook-public'),
]
