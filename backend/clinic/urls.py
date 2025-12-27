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
    # Dashboard
    path('dashboard/', views.dashboard_stats, name='dashboard'),
    
    # Patients
    path('patients/', views.patient_list, name='patient_list'),
    path('patients/<int:pk>/', views.patient_detail, name='patient_detail'),
    
    # Owners
    path('owners/', views.owner_list, name='owner_list'),
    path('owners/<int:pk>/', views.owner_detail, name='owner_detail'),
    
    # Medical Records
    path('medical-records/', views.medical_record_list, name='medical_record_list'),
    path('medical-records/<int:pk>/', views.medical_record_detail, name='medical_record_detail'),
    
    # Vaccinations
    path('vaccinations/', views.vaccination_list, name='vaccination_list'),
    path('vaccinations/<int:pk>/', views.vaccination_detail, name='vaccination_detail'),
    
    # Payments
    path('payments/', views.payment_list, name='payment_list'),
    path('payments/<int:pk>/', views.payment_detail, name='payment_detail'),
    
    # ✅ FIXED: Added missing passbooks endpoints
    path('passbooks/', views.passbook_list, name='passbook_list'),
    path('passbooks/<int:pk>/', views.passbook_detail, name='passbook_detail'),
    
    # ✅ FIXED: Added missing prescriptions endpoints
    path('prescriptions/', views.prescription_list, name='prescription_list'),
    path('prescriptions/<int:pk>/', views.prescription_detail, name='prescription_detail'),
]
