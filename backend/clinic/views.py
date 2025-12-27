"""
Clinic App Views - Basic CRUD ViewSets
"""
from rest_framework import viewsets, permissions, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import get_user_model
from django.db.models import Q
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys

from .models import (
    Owner, Patient, MedicalRecord, Vaccination, 
    LabTest, Payment,Prescription
)
from .serializers import (
    OwnerSerializer, PatientSerializer, MedicalRecordSerializer,
    VaccinationSerializer, LabTestSerializer, PaymentSerializer,
    UserSerializer,PrescriptionSerializer
)
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.shortcuts import get_object_or_404
from .models import PetPassbook, Patient
from .serializers import PassbookSerializer, PassbookPublicSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
}

@api_view(['GET'])
@permission_classes([AllowAny])
def current_user(request):
    """Return current authenticated user info"""
    user = request.user
    return Response({
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'role': getattr(user, 'role', 'doctor'),
        'phone': getattr(user, 'phone', ''),
    })

User = get_user_model()


# ============================================================================
# Authentication Views
# ============================================================================

class LoginView(TokenObtainPairView):
    """Custom login view"""
    permission_classes = [AllowAny]


class LogoutView(APIView):
    """Logout view"""
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        return Response({'message': 'Logged out successfully'})


class RefreshTokenView(APIView):
    """Refresh token view"""
    permission_classes = [AllowAny]
    
    def post(self, request):
        # This will be handled by JWT refresh endpoint
        return Response({'message': 'Use /api/token/refresh/ instead'})


class CurrentUserView(APIView):
    """Get current user details"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)


# ============================================================================
# CRUD ViewSets
# ============================================================================

class OwnerViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Owner (Pet Owner) CRUD operations
    """
    queryset = Owner.objects.all()
    serializer_class = OwnerSerializer
    permission_classes = [AllowAny]  # Change to IsAuthenticated in production
    
    def get_queryset(self):
        queryset = Owner.objects.all().order_by('-created_at')
        
        # Search filter
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                first_name__icontains=search
            ) | queryset.filter(
                last_name__icontains=search
            ) | queryset.filter(
                phone__icontains=search
            )
        
        return queryset

class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    permission_classes = [AllowAny]
    
    def perform_create(self, serializer):
        # Handle photo upload and resize
        photo = self.request.FILES.get('photo')
        if photo:
            photo = self.resize_image(photo)

        # ✅ FIX: Check if user is authenticated before setting created_by
        if self.request.user and self.request.user.is_authenticated:
            serializer.save(created_by=self.request.user, photo=photo if photo else None)
        else:
            serializer.save(photo=photo if photo else None)  # Don't set created_by for anonymous
        
    
    def perform_update(self, serializer):
        photo = self.request.FILES.get('photo')
        if photo:
            photo = self.resize_image(photo)
            serializer.save(photo=photo)
        else:
            serializer.save()
    
    def resize_image(self, photo):
        """Resize image to max 300x300, maintain aspect ratio, compress"""
        try:
            img = Image.open(photo)
            
            # Convert RGBA to RGB if needed
            if img.mode in ('RGBA', 'LA', 'P'):
                background = Image.new('RGB', img.size, (255, 255, 255))
                background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                img = background
            
            # Resize maintaining aspect ratio
            img.thumbnail((300, 300), Image.Resampling.LANCZOS)
            
            # Save to BytesIO
            output = BytesIO()
            img.save(output, format='JPEG', quality=85, optimize=True)
            output.seek(0)
            
            # Create new InMemoryUploadedFile
            return InMemoryUploadedFile(
                output,
                'ImageField',
                f"{photo.name.split('.')[0]}_resized.jpg",
                'image/jpeg',
                sys.getsizeof(output),
                None
            )
        except Exception as e:
            print(f"Error resizing image: {e}")
            return photo  # Return original if resize fails
    
    @action(detail=True, methods=['get'])
    def passbook(self, request, pk=None):
        """Get patient passbook/history"""
        patient = self.get_object()
        # TODO: Implement passbook generation
        return Response({'message': 'Passbook feature coming soon'})
    
    @action(detail=True, methods=['post'])
    def share_url(self, request, pk=None):
        """Create share URL for patient"""
        patient = self.get_object()
        # TODO: Implement share URL generation
        return Response({'message': 'Share URL feature coming soon'})
    
    @action(detail=True, methods=['get'])
    def qr_code(self, request, pk=None):
        """Generate QR code for patient"""
        patient = self.get_object()
        # TODO: Implement QR code generation
        return Response({'message': 'QR code feature coming soon'})


class MedicalRecordViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Medical Record CRUD operations
    """
    queryset = MedicalRecord.objects.all()
    serializer_class = MedicalRecordSerializer
    permission_classes = [AllowAny]  # Change to IsAuthenticated in production
    
    def get_queryset(self):
        queryset = MedicalRecord.objects.select_related('patient', 'doctor').all().order_by('-visit_date')
        
        # Filter by patient
        patient_id = self.request.query_params.get('patient', None)
        if patient_id:
            queryset = queryset.filter(patient_id=patient_id)
        
        return queryset


class VaccinationViewSet(viewsets.ModelViewSet):
    queryset = Vaccination.objects.all()
    serializer_class = VaccinationSerializer
    permission_classes = [AllowAny]
    
    def create(self, request, *args, **kwargs):
        print("\n" + "=" * 70)
        print("🔍 VACCINATION CREATE REQUEST")
        print("=" * 70)
        print("📥 Request Data:", request.data)
        print("=" * 70)
        
        serializer = self.get_serializer(data=request.data)
        
        if not serializer.is_valid():
            print("❌ VALIDATION ERRORS:")
            print(serializer.errors)
            print("=" * 70 + "\n")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        print("✅ Validation passed! Creating vaccination...")
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        print("✅ Vaccination created successfully!")
        print("=" * 70 + "\n")
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class LabTestViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Lab Test CRUD operations
    """
    queryset = LabTest.objects.all()
    serializer_class = LabTestSerializer
    permission_classes = [AllowAny]  # Change to IsAuthenticated in production
    
    def get_queryset(self):
        queryset = LabTest.objects.select_related('patient', 'medical_record').all().order_by('-test_date')
        
        # Filter by patient
        patient_id = self.request.query_params.get('patient', None)
        if patient_id:
            queryset = queryset.filter(patient_id=patient_id)
        
        return queryset


class PaymentViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Payment CRUD operations
    """
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [AllowAny]  # Change to IsAuthenticated in production
    
    def get_queryset(self):
        queryset = Payment.objects.select_related('medical_record', 'patient').all().order_by('-payment_date')
        
        # Filter by patient
        patient_id = self.request.query_params.get('patient', None)
        if patient_id:
            queryset = queryset.filter(patient_id=patient_id)
        
        # Filter by payment status
        status = self.request.query_params.get('status', None)
        if status:
            queryset = queryset.filter(payment_status=status)
        
        return queryset

class PrescriptionViewSet(viewsets.ModelViewSet):
    queryset = Prescription.objects.all().select_related(
        'medical_record__patient', 'medical_record__doctor'
    ).order_by('-created_at')  # ← Changed from 'prescribed_date'
    serializer_class = PrescriptionSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['medication_name', 'medical_record__patient__name', 'instructions']
    ordering_fields = ['created_at']  # ← Changed from 'prescribed_date'
    
    def get_queryset(self):
        queryset = super().get_queryset()
        patient_id = self.request.query_params.get('patient', None)
        medical_record_id = self.request.query_params.get('medical_record', None)
        
        if patient_id:
            queryset = queryset.filter(medical_record__patient_id=patient_id)
        if medical_record_id:
            queryset = queryset.filter(medical_record_id=medical_record_id)
            
        return queryset
# ============================================================================
# Additional Views (Stubs for future implementation)
# ============================================================================

class WhisperTranscribeView(APIView):
    """Voice transcription using Whisper"""
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        return Response({'message': 'Whisper transcription coming soon'})


class PatientPassbookView(APIView):
    """Generate patient passbook"""
    permission_classes = [AllowAny]
    
    def get(self, request, pk):
        return Response({'message': 'Passbook feature coming soon'})


class CreateShareURLView(APIView):
    """Create share URL for patient"""
    permission_classes = [IsAuthenticated]
    
    def post(self, request, pk):
        return Response({'message': 'Share URL feature coming soon'})


class PatientQRCodeView(APIView):
    """Generate QR code for patient"""
    permission_classes = [AllowAny]
    
    def get(self, request, pk):
        return Response({'message': 'QR code feature coming soon'})


class GeneratePrescriptionPDFView(APIView):
    """Generate prescription PDF"""
    permission_classes = [AllowAny]
    
    def get(self, request, record_id):
        return Response({'message': 'Prescription PDF coming soon'})


class GenerateVaccinationPDFView(APIView):
    """Generate vaccination certificate PDF"""
    permission_classes = [AllowAny]
    
    def get(self, request, vaccination_id):
        return Response({'message': 'Vaccination PDF coming soon'})


class GenerateHealthCertificatePDFView(APIView):
    """Generate health certificate PDF"""
    permission_classes = [AllowAny]
    
    def get(self, request, patient_id):
        return Response({'message': 'Health certificate PDF coming soon'})


class GenerateLabReportPDFView(APIView):
    """Generate lab report PDF"""
    permission_classes = [AllowAny]
    
    def get(self, request, lab_test_id):
        return Response({'message': 'Lab report PDF coming soon'})


class SharedURLAccessView(APIView):
    """Access shared patient data"""
    permission_classes = [AllowAny]
    
    def get(self, request, short_code):
        return Response({'message': 'Shared URL access coming soon'})


class AnalyticsOverviewView(APIView):
    """Analytics dashboard overview"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        return Response({'message': 'Analytics coming soon'})


class RevenueAnalyticsView(APIView):
    """Revenue analytics"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        return Response({'message': 'Revenue analytics coming soon'})


class SubscriptionStatusView(APIView):
    """Check subscription status"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        return Response({'message': 'Subscription feature coming soon'})


class UpgradeSubscriptionView(APIView):
    """Upgrade subscription"""
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        return Response({'message': 'Upgrade feature coming soon'})


class GlobalSearchView(APIView):
    """Global search across all entities"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        query = request.query_params.get('q', '')
        return Response({
            'message': 'Search feature coming soon',
            'query': query
        })

# ============================================
# FILE: backend/clinic/views.py (ADD THESE VIEWSETS)
# ============================================

class PassbookViewSet(viewsets.ModelViewSet):
    """Admin management of pet passbooks (authenticated)"""
    queryset = PetPassbook.objects.all()
    serializer_class = PassbookSerializer
    permission_classes = [IsAuthenticated]
    
    @action(detail=True, methods=['post'])
    def activate(self, request, pk=None):
        """Activate subscription for X months"""
        passbook = self.get_object()
        months = int(request.data.get('months', 1))
        passbook.activate_subscription(duration_months=months)
        return Response({
            'message': 'Subscription activated',
            'subscription_end': passbook.subscription_end,
            'is_active': passbook.is_active
        })
    
    @action(detail=True, methods=['post'])
    def regenerate_token(self, request, pk=None):
        """Regenerate QR code token"""
        passbook = self.get_object()
        new_token = passbook.regenerate_token()
        serializer = self.get_serializer(passbook)
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'])
    def create_for_patient(self, request):
        """Create passbook for a patient"""
        patient_id = request.data.get('patient_id')
        patient = get_object_or_404(Patient, id=patient_id)
        
        # Check if passbook already exists
        passbook, created = PetPassbook.objects.get_or_create(patient=patient)
        
        if created:
            # Activate for 1 month by default
            passbook.activate_subscription(duration_months=1)
        
        serializer = self.get_serializer(passbook, context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)


class PassbookPublicViewSet(viewsets.ViewSet):
    """Public passbook access (no authentication required)"""
    permission_classes = [AllowAny]
    
    def retrieve(self, request, token=None):
        """Get passbook by access token"""
        try:
            passbook = PetPassbook.objects.select_related('patient').get(access_token=token)
            
            # Record access
            passbook.record_access()
            
            # Serialize with subscription validation
            serializer = PassbookPublicSerializer(passbook)
            
            return Response({
                'success': True,
                'data': serializer.data
            })
            
        except PetPassbook.DoesNotExist:
            return Response({
                'success': False,
                'error': 'Invalid or expired passbook link'
            }, status=status.HTTP_404_NOT_FOUND)
