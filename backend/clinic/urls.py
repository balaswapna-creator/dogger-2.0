# backend/clinic/urls.py - Complete Fixed Version

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'owners', views.OwnerViewSet)
router.register(r'patients', views.PatientViewSet)
router.register(r'medical-records', views.MedicalRecordViewSet)
router.register(r'vaccinations', views.VaccinationViewSet)
router.register(r'lab-tests', views.LabTestViewSet)
router.register(r'payments', views.PaymentViewSet)
router.register(r'prescriptions', views.PrescriptionViewSet)
router.register(r'passbooks', views.PassbookViewSet)

urlpatterns = [
    # ✅ Authentication
    path('token/', views.LoginView.as_view(), name='token_obtain_pair'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('auth/me/', views.current_user, name='current_user'),
    
    # ✅ CRITICAL FIX - Dashboard Stats API
    path('dashboard/', views.dashboard_stats, name='dashboard_stats'),
    
    # ✅ Public Passbook Access (no auth required)
    path('passbooks/public/<uuid:token>/', 
         views.PassbookPublicViewSet.as_view({'get': 'retrieve'}), 
         name='passbook_public'),
    
    # ✅ Router URLs (all CRUD endpoints)
    path('', include(router.urls)),
]