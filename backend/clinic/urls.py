"""
Clinic App URLs
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'owners', views.OwnerViewSet, basename='owner')
router.register(r'patients', views.PatientViewSet, basename='patient')
router.register(r'medical-records', views.MedicalRecordViewSet, basename='medicalrecord')
router.register(r'vaccinations', views.VaccinationViewSet, basename='vaccination')
router.register(r'lab-tests', views.LabTestViewSet, basename='labtest')
router.register(r'payments', views.PaymentViewSet, basename='payment')
router.register(r'prescriptions', views.PrescriptionViewSet, basename='prescription')
router.register(r'passbooks', views.PassbookViewSet, basename='passbook')

urlpatterns = [
    # Router URLs (all CRUD endpoints)
    path('', include(router.urls)),
    
    # Custom endpoints
    path('dashboard/stats/', views.dashboard_stats, name='dashboard-stats'),
    path('auth/login/', views.LoginView.as_view(), name='login'),
    path('auth/logout/', views.LogoutView.as_view(), name='logout'),
    path('auth/user/', views.current_user, name='current-user'),
    
    # ✅ Passbook public access - accepts any string token
    path('passbooks-public/<str:access_token>/', 
         views.passbook_public_retrieve, 
         name='passbook-public-retrieve'),
    # Activate passbook (temporary)
    path('passbooks/<uuid:passbook_id>/activate/', views.activate_passbook, name='activate_passbook'),
]