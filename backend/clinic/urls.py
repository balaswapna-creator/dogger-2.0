"""
Clinic App URLs - Complete and Clean
✅ FIXED VERSION - No Conflicts
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Create router for ViewSets
router = DefaultRouter()
router.register(r'patients', views.PatientViewSet, basename='patient')
router.register(r'owners', views.OwnerViewSet, basename='owner')
router.register(r'medical-records', views.MedicalRecordViewSet, basename='medicalrecord')
router.register(r'payments', views.PaymentViewSet, basename='payment')
router.register(r'vaccinations', views.VaccinationViewSet, basename='vaccination')
router.register(r'prescriptions', views.PrescriptionViewSet, basename='prescription')
router.register(r'passbooks', views.PassbookViewSet, basename='passbook')

urlpatterns = [
    # ✅ Dashboard Stats
    path('dashboard/', views.dashboard_stats, name='dashboard'),
    
    # ✅ Include all ViewSet routes
    path('', include(router.urls)),
    
    # ✅ Public Passbook Access (No Auth Required)
    path('passbook/<uuid:token>/', 
         views.PassbookPublicViewSet.as_view({'get': 'retrieve'}), 
         name='passbook-public'),
]