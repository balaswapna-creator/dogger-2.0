"""
Clinic App Views - Complete with Dashboard Stats
✅ FIXED VERSION - Indentation Corrected
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
        """✅ FIXED INDENTATION"""
        try:
            photo = self.request.FILES.get('photo')
            if photo:
                photo = self.resize_image(photo)
        
            save_kwargs = {}
            if photo:
                save_kwargs['photo'] = photo
        
            # Don't set created_by for now
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
    serializer_class = PassbookSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        """Optimize query with select_related to avoid N+1 queries"""
        return PetPassbook.objects.select_related(
            'patient',
            'patient__owner'
        ).all()
    
    def create(self, request, *args, **kwargs):
        patient_id = request.data.get('patient_id')
        
        if not patient_id:
            return Response(
                {'error': 'patient_id is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Check if passbook already exists
        passbook = PetPassbook.objects.filter(patient_id=patient_id).first()
        if passbook:
            serializer = self.get_serializer(passbook, context={'request': request})
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        # Create new passbook
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class PassbookPublicViewSet(viewsets.ReadOnlyModelViewSet):
    """Public passbook access (no authentication)"""
    permission_classes = [AllowAny]
    queryset = PetPassbook.objects.select_related('patient__owner').all()
    serializer_class = PassbookPublicSerializer
    lookup_field = 'access_token'
    lookup_value_regex = '[^/]+'  # ✅ This allows any characters in the URL
    
    def retrieve(self, request, access_token=None):
        """Get passbook by access token"""
        try:
            # Get the passbook using the access_token
            passbook = PetPassbook.objects.select_related(
                'patient__owner'
            ).get(access_token=access_token)
            
            # Record the access
            passbook.record_access()
            
            # Serialize the data
            serializer = self.get_serializer(passbook, context={'request': request})
            
            return Response({
                'success': True,
                'data': serializer.data
            })
            
        except PetPassbook.DoesNotExist:
            return Response({
                'success': False,
                'error': 'Invalid or expired passbook link'
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(f"Error retrieving passbook: {e}")
            import traceback
            traceback.print_exc()
            return Response({
                'success': False,
                'error': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    def _mask_phone(self, phone):
        """Mask phone number for privacy"""
        if phone and len(phone) > 4:
            return phone[:4] + "****" + phone[-2:]
        return phone or 'N/A'
    
    def _get_vaccinations(self, passbook):
        """Get vaccination records"""
        if not passbook.is_active:
            return []
        
        try:
            vaccinations = Vaccination.objects.filter(
                patient=passbook.patient
            ).order_by('-date_administered')[:10]
            
            return [{
                'vaccine_name': v.vaccine_name,
                'date_administered': v.date_administered.isoformat() if v.date_administered else None,
                'next_due_date': v.next_due_date.isoformat() if v.next_due_date else None,
                'certificate_number': v.certificate_number,
                'administered_by': v.administered_by or 'Dr. A. Balasubramanan'
            } for v in vaccinations]
        except Exception as e:
            print(f"Error fetching vaccinations: {e}")
            return []
    
    def _get_consultations(self, passbook):
        """Get medical records"""
        if not passbook.is_active:
            return []
        
        try:
            records = MedicalRecord.objects.filter(
                patient=passbook.patient
            ).order_by('-visit_date')[:10]
            
            return [{
                'visit_date': r.visit_date.isoformat() if r.visit_date else None,
                'visit_type': r.visit_type,
                'chief_complaint': r.chief_complaint,
                'diagnosis': r.diagnosis,
                'treatment_plan': r.treatment_plan,
                'temperature': float(r.temperature) if r.temperature else None,
                'weight': float(r.weight) if r.weight else None
            } for r in records]
        except Exception as e:
            print(f"Error fetching consultations: {e}")
            return []

# ============================================================================
# PASSBOOK PUBLIC VIEW (Add this at the END of views.py)
# ============================================================================

@api_view(['GET'])
@permission_classes([AllowAny])
def passbook_public_retrieve(request, access_token):
    """Get passbook by access token - public access"""
    try:
        # Find passbook by token
        passbook = PetPassbook.objects.select_related('patient__owner').get(
            access_token=access_token
        )
        
        # Record access
        try:
            passbook.record_access()
        except:
            pass  # Continue even if record_access fails
        
        # Build response with all patient data
        patient = passbook.patient
        owner = patient.owner if patient else None
        
        # Calculate age
        age_str = 'N/A'
        if patient and patient.date_of_birth:
            dob = patient.date_of_birth
            today = timezone.now().date()
            years = today.year - dob.year
            months = today.month - dob.month
            if months < 0:
                years -= 1
                months += 12
            age_str = f"{years} years, {months} months" if years > 0 else f"{months} months"
        
        # Get vaccinations
        vaccinations = []
        if passbook.is_active and patient:
            try:
                vacc_list = Vaccination.objects.filter(patient=patient).order_by('-date_administered')[:10]
                vaccinations = [{
                    'vaccine_name': v.vaccine_name,
                    'date_administered': v.date_administered.isoformat() if v.date_administered else None,
                    'next_due_date': v.next_due_date.isoformat() if v.next_due_date else None,
                    'certificate_number': v.certificate_number,
                    'administered_by': v.administered_by or 'Dr. A. Balasubramanan'
                } for v in vacc_list]
            except Exception as e:
                print(f"Error fetching vaccinations: {e}")
        
        # Get medical records
        consultations = []
        if passbook.is_active and patient:
            try:
                records = MedicalRecord.objects.filter(patient=patient).order_by('-visit_date')[:10]
                consultations = [{
                    'visit_date': r.visit_date.isoformat() if r.visit_date else None,
                    'visit_type': r.visit_type,
                    'chief_complaint': r.chief_complaint,
                    'diagnosis': r.diagnosis,
                    'treatment_plan': r.treatment_plan,
                    'temperature': float(r.temperature) if r.temperature else None,
                    'weight': float(r.weight) if r.weight else None
                } for r in records]
            except Exception as e:
                print(f"Error fetching consultations: {e}")
        
        # Build photo URL
        photo_url = None
        if patient and patient.photo:
            try:
                photo_url = request.build_absolute_uri(patient.photo.url)
            except:
                pass
        
        # Mask phone number
        owner_phone = 'N/A'
        if owner and owner.phone:
            phone = owner.phone
            if len(phone) > 4:
                owner_phone = phone[:4] + "****" + phone[-2:]
            else:
                owner_phone = phone
        
        # Return data
        return Response({
            # Clinic info
            'clinic_name': 'Sri Adithya Pet Clinic',
            'clinic_address': 'No:16,Sriram Nagar, Theni, Tamil Nadu - 625531',
            
            # Patient info
            'pet_name': patient.pet_name if patient else 'N/A',
            'species': patient.species if patient else 'N/A',
            'breed': patient.breed if patient else 'N/A',
            'gender': patient.gender if patient else 'N/A',
            'date_of_birth': patient.date_of_birth.isoformat() if patient and patient.date_of_birth else None,
            'color': patient.color if patient else 'N/A',
            'age': age_str,
            'photo': photo_url,
            
            # Owner info (masked)
            'owner_name': owner.name if owner else 'N/A',
            'owner_phone': owner_phone,
            
            # Medical data
            'vaccinations': vaccinations,
            'consultations': consultations,
            
            # Subscription
            'is_active': passbook.is_active,
            'subscription_end': (timezone.now() + timedelta(days=365)).isoformat(),
            'days_remaining': 365,
        })
        
    except PetPassbook.DoesNotExist:
        return Response({
            'error': 'Invalid or expired passbook link'
        }, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        print(f"Passbook error: {e}")
        import traceback
        traceback.print_exc()
        return Response({
            'error': str(e)
        }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['POST'])
@permission_classes([AllowAny])
def activate_passbook(request, passbook_id):
    """Temporary endpoint to activate a passbook subscription"""
    try:
        passbook = PetPassbook.objects.get(id=passbook_id)
        passbook.activate_subscription(duration_months=12)  # Activate for 12 months
        
        return Response({
            'success': True,
            'message': f'Passbook activated for {passbook.patient.pet_name}',
            'subscription_end': passbook.subscription_end,
            'is_active': passbook.is_active,
            'access_token': str(passbook.access_token)
        })
    except PetPassbook.DoesNotExist:
        return Response({
            'success': False,
            'error': 'Passbook not found'
        }, status=404)
    except Exception as e:
        return Response({
            'success': False,
            'error': str(e)
        }, status=500)