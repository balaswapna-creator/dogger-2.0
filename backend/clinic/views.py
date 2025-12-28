"""
Clinic App Views - Complete with Dashboard Stats
✅ FIXED VERSION
"""
from rest_framework import viewsets, permissions, filters, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import get_user_model
from django.db.models import Q, Count, Sum
from django.shortcuts import get_object_or_404
from django.utils import timezone
from datetime import timedelta
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import sys

from .models import (
    Owner, Patient, MedicalRecord, Vaccination, 
    LabTest, Payment, Prescription, PetPassbook
)
from .serializers import (
    OwnerSerializer, PatientSerializer, MedicalRecordSerializer,
    VaccinationSerializer, LabTestSerializer, PaymentSerializer,
    UserSerializer, PrescriptionSerializer, PassbookSerializer,
    PassbookPublicSerializer
)

User = get_user_model()


# ============================================================================
# ✅ DASHBOARD STATS (MISSING FUNCTION)
# ============================================================================

@api_view(['GET'])
@permission_classes([AllowAny])  # Change to IsAuthenticated in production
def dashboard_stats(request):
    """Return dashboard statistics"""
    try:
        # Get date ranges
        today = timezone.now().date()
        week_ago = today - timedelta(days=7)
        month_ago = today - timedelta(days=30)
        
        # Total counts
        total_patients = Patient.objects.filter(is_active=True).count()
        total_owners = Owner.objects.count()
        
        # This week
        patients_this_week = Patient.objects.filter(created_at__date__gte=week_ago).count()
        consultations_this_week = MedicalRecord.objects.filter(visit_date__date__gte=week_ago).count()
        
        # Revenue
        revenue_this_month = Payment.objects.filter(
            payment_date__date__gte=month_ago,
            payment_status='completed'
        ).aggregate(total=Sum('amount'))['total'] or 0
        
        # Upcoming vaccinations
        upcoming_vaccinations = Vaccination.objects.filter(
            next_due_date__gte=today,
            next_due_date__lte=today + timedelta(days=30)
        ).count()
        
        return Response({
            'total_patients': total_patients,
            'total_owners': total_owners,
            'patients_this_week': patients_this_week,
            'consultations_this_week': consultations_this_week,
            'revenue_this_month': float(revenue_this_month),
            'upcoming_vaccinations': upcoming_vaccinations,
        })
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


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


class CurrentUserView(APIView):
    """Get current user details"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)


@api_view(['GET'])
@permission_classes([AllowAny])
def current_user(request):
    """Return current authenticated user info"""
    user = request.user
    return Response({
        'id': str(user.id),
        'username': user.username,
        'email': user.email,
        'role': getattr(user, 'role', 'doctor'),
        'phone': getattr(user, 'phone', ''),
    })


# ============================================================================
# CRUD ViewSets
# ============================================================================

class OwnerViewSet(viewsets.ModelViewSet):
    """ViewSet for Owner CRUD operations"""
    queryset = Owner.objects.all()
    serializer_class = OwnerSerializer
    permission_classes = [AllowAny]
    
    def get_queryset(self):
        queryset = Owner.objects.all().order_by('-created_at')
        
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) | Q(phone__icontains=search)
            )
        
        return queryset


class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    permission_classes = [AllowAny]
    
    def perform_create(self, serializer):
    try:
        photo = self.request.FILES.get('photo')
        if photo:
            photo = self.resize_image(photo)
        
        save_kwargs = {}
        if photo:
            save_kwargs['photo'] = photo
        
        # Don't set created_by for now - remove this field requirement
        # if self.request.user.is_authenticated:
        #     save_kwargs['created_by'] = self.request.user
        
        serializer.save(**save_kwargs)
    except Exception as e:
        print(f"❌ Error creating patient: {e}")
        raise
    
    def perform_update(self, serializer):
        photo = self.request.FILES.get('photo')
        if photo:
            photo = self.resize_image(photo)
            serializer.save(photo=photo)
        else:
            serializer.save()
    
    def resize_image(self, photo):
        """Resize image to max 300x300"""
        try:
            img = Image.open(photo)
            
            if img.mode in ('RGBA', 'LA', 'P'):
                background = Image.new('RGB', img.size, (255, 255, 255))
                if img.mode == 'RGBA':
                    background.paste(img, mask=img.split()[-1])
                else:
                    background.paste(img)
                img = background
            
            img.thumbnail((300, 300), Image.Resampling.LANCZOS)
            
            output = BytesIO()
            img.save(output, format='JPEG', quality=85, optimize=True)
            output.seek(0)
            
            file_size = output.getbuffer().nbytes
            
            return InMemoryUploadedFile(
                output,
                'ImageField',
                f"{photo.name.split('.')[0]}_resized.jpg",
                'image/jpeg',
                file_size,
                None
            )
        except Exception as e:
            print(f"Error resizing image: {e}")
            return photo


class MedicalRecordViewSet(viewsets.ModelViewSet):
    """ViewSet for Medical Record CRUD"""
    queryset = MedicalRecord.objects.all()
    serializer_class = MedicalRecordSerializer
    permission_classes = [AllowAny]
    
    def get_queryset(self):
        queryset = MedicalRecord.objects.select_related('patient', 'doctor').all().order_by('-visit_date')
        
        patient_id = self.request.query_params.get('patient', None)
        if patient_id:
            queryset = queryset.filter(patient_id=patient_id)
        
        return queryset


class VaccinationViewSet(viewsets.ModelViewSet):
    queryset = Vaccination.objects.all()
    serializer_class = VaccinationSerializer
    permission_classes = [AllowAny]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class LabTestViewSet(viewsets.ModelViewSet):
    """ViewSet for Lab Test CRUD"""
    queryset = LabTest.objects.all()
    serializer_class = LabTestSerializer
    permission_classes = [AllowAny]
    
    def get_queryset(self):
        queryset = LabTest.objects.select_related('patient', 'medical_record').all().order_by('-ordered_date')
        
        patient_id = self.request.query_params.get('patient', None)
        if patient_id:
            queryset = queryset.filter(patient_id=patient_id)
        
        return queryset


class PaymentViewSet(viewsets.ModelViewSet):
    """ViewSet for Payment CRUD"""
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [AllowAny]
    
    def get_queryset(self):
        queryset = Payment.objects.select_related('medical_record', 'patient').all().order_by('-payment_date')
        
        patient_id = self.request.query_params.get('patient', None)
        if patient_id:
            queryset = queryset.filter(patient_id=patient_id)
        
        status_filter = self.request.query_params.get('status', None)
        if status_filter:
            queryset = queryset.filter(payment_status=status_filter)
        
        return queryset


class PrescriptionViewSet(viewsets.ModelViewSet):
    queryset = Prescription.objects.all().select_related(
        'medical_record__patient', 'medical_record__doctor'
    ).order_by('-created_at')
    serializer_class = PrescriptionSerializer
    permission_classes = [AllowAny]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['medication_name', 'medical_record__patient__pet_name', 'instructions']
    ordering_fields = ['created_at']
    
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
# ✅ PASSBOOK VIEWSETS
# ============================================================================

class PassbookViewSet(viewsets.ModelViewSet):
    """Admin management of pet passbooks"""
    queryset = PetPassbook.objects.all()
    serializer_class = PassbookSerializer
    permission_classes = [AllowAny]  # Change to IsAuthenticated in production
    
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
        
        passbook, created = PetPassbook.objects.get_or_create(patient=patient)
        
        if created:
            passbook.activate_subscription(duration_months=1)
        
        serializer = self.get_serializer(passbook, context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED if created else status.HTTP_200_OK)


class PassbookPublicViewSet(viewsets.ViewSet):
    """Public passbook access (no authentication)"""
    permission_classes = [AllowAny]
    
    def retrieve(self, request, token=None):
        """Get passbook by access token"""
        try:
            passbook = PetPassbook.objects.select_related('patient').get(access_token=token)
            passbook.record_access()
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