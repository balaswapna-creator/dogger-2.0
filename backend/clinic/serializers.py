"""
Clinic App Serializers - Complete and Fixed

"""
from rest_framework import serializers
from .models import (
    User, Owner, Patient, MedicalRecord, Prescription,
    Vaccination, LabTest, SharedURL, Payment, Subscription, 
    AuditLog, PetPassbook
)


# ============================================================================
# USER SERIALIZER
# ============================================================================

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'role', 'phone']
        read_only_fields = ['id']


# ============================================================================
# OWNER SERIALIZER
# ============================================================================
class OwnerSerializer(serializers.ModelSerializer):
    patient_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Owner
        fields = [
            'id', 'name', 'phone', 'email', 'address', 
            'city', 'whatsapp_number', 'created_at', 'updated_at', 
            'created_by', 'patient_count'
        ]
        read_only_fields = ['created_at', 'updated_at', 'patient_count']
    
    def get_patient_count(self, obj):
        """Count number of patients (pets) for this owner"""
        return obj.patients.count()


# ============================================================================
# PATIENT SERIALIZER
# ============================================================================

class PatientSerializer(serializers.ModelSerializer):
    owner_name = serializers.CharField(source='owner.name', read_only=True)
    last_visit = serializers.SerializerMethodField()
    
    class Meta:
        model = Patient
        fields = [
            'id',
            'pet_name',
            'species', 
            'breed',
            'date_of_birth',
            'gender',
            'color',
            'owner',
            'owner_name',
            'photo',
            'qr_code',
            'created_at',
            'updated_at',
            'last_visit'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'qr_code']
    
    def get_last_visit(self, obj):
        """Calculate last visit from medical records"""
        try:
            latest_record = obj.medicalrecord_set.order_by('-visit_date').first()
            if latest_record:
                return latest_record.visit_date.isoformat()
            return obj.created_at.isoformat() if obj.created_at else None
        except Exception:
            return None

# ============================================================================
# MEDICAL RECORD SERIALIZER
# ============================================================================

class MedicalRecordSerializer(serializers.ModelSerializer):
    patient_name = serializers.SerializerMethodField()
    doctor_name = serializers.SerializerMethodField()

    class Meta:
        model = MedicalRecord
        fields = [
            'id', 'patient', 'patient_name', 'visit_date', 'visit_type',
            'chief_complaint', 'history', 'clinical_notes', 'diagnosis',
            'treatment_plan', 'temperature', 'weight', 'heart_rate',
            'next_visit_date', 'follow_up_notes', 'consultation_fee',
            'doctor', 'doctor_name', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at', 'doctor']

    def get_patient_name(self, obj):
        return obj.patient.pet_name if obj.patient else None

    def get_doctor_name(self, obj):
        return obj.doctor.get_full_name() if obj.doctor else None


# ============================================================================
# PRESCRIPTION SERIALIZER
# ============================================================================

# FILE: backend/clinic/serializers.py
# Find and REPLACE your PrescriptionSerializer

from rest_framework import serializers
from .models import Prescription, PrescriptionItem, Patient, MedicalRecord


class PrescriptionItemSerializer(serializers.ModelSerializer):
    """Serializer for individual medications"""
    
    class Meta:
        model = PrescriptionItem
        fields = [
            'id', 
            'medication_name', 
            'dosage', 
            'frequency', 
            'duration', 
            'instructions',
            'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class PrescriptionListSerializer(serializers.ModelSerializer):
    """Simplified serializer for listing prescriptions"""
    patient_name = serializers.SerializerMethodField()
    medication_count = serializers.SerializerMethodField()
    medications_summary = serializers.SerializerMethodField()
    
    class Meta:
        model = Prescription
        fields = [
            'id',
            'patient_name',
            'medication_count',
            'medications_summary',
            'notes',
            'created_at'
        ]
    
    def get_patient_name(self, obj):
        """Safely get patient name"""
        try:
            if obj.patient:
                return obj.patient.pet_name
            elif obj.medical_record and obj.medical_record.patient:
                return obj.medical_record.patient.pet_name
        except Exception as e:
            print(f"Error getting patient_name: {e}")
        return "Unknown"
    
    def get_medication_count(self, obj):
        """Safely get medication count"""
        try:
            count = obj.items.count()
            if count > 0:
                return count
            # Check legacy single drug
            if obj.medication_name:
                return 1
        except Exception as e:
            print(f"Error getting medication_count: {e}")
        return 0
    
    def get_medications_summary(self, obj):
        """Get summary of medications"""
        try:
            items = obj.items.all()[:3]
            if items:
                names = [item.medication_name for item in items]
                count = obj.items.count()
                if count > 3:
                    names.append(f"+ {count - 3} more")
                return ", ".join(names)
            # Check legacy single drug
            if obj.medication_name:
                return obj.medication_name
        except Exception as e:
            print(f"Error getting medications_summary: {e}")
        return "No medications"


class PrescriptionSerializer(serializers.ModelSerializer):
    patient_name = serializers.SerializerMethodField()
    medicine_count = serializers.SerializerMethodField()
    medicines = serializers.JSONField(required=False)  # 🔥 ADD THIS
    
    class Meta:
        model = Prescription
        fields = [
            'id',
            'medical_record',
            'patient_name',
            'medicine_count',
            'medicines',  # 🔥 ADD THIS
            'created_at',
            'updated_at',
            'medication_name',
            'dosage',
            'frequency',
            'duration',
            'instructions',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'patient_name', 'medicine_count']
    
    def get_patient_name(self, obj):
        try:
            if obj.medical_record and obj.medical_record.patient:
                return obj.medical_record.patient.name
            return 'Unknown'
        except:
            return 'Unknown'
    
    def get_medicine_count(self, obj):
        if obj.medicines and isinstance(obj.medicines, list):
            return len(obj.medicines)
        return 1 if obj.medication_name else 0
    
    def to_representation(self, instance):
        """Ensure medicines is always a list."""
        representation = super().to_representation(instance)
        
        medicines = representation.get('medicines')
        if medicines is None:
            representation['medicines'] = []
        elif isinstance(medicines, str):
            try:
                import json
                representation['medicines'] = json.loads(medicines)
            except:
                representation['medicines'] = []
        elif not isinstance(medicines, list):
            representation['medicines'] = []
        
        return representation

# ============================================================================
# VACCINATION SERIALIZER
# ============================================================================

class VaccinationSerializer(serializers.ModelSerializer):
    patient_name = serializers.SerializerMethodField()
    owner_name = serializers.SerializerMethodField()
    
    class Meta:
        model = Vaccination
        fields = [
            'id', 'patient', 'patient_name', 'owner_name',
            'vaccine_name', 'manufacturer', 'batch_number',
            'date_administered', 'next_due_date',
            'administered_by', 'notes', 'certificate_number',
            'created_at'
        ]
        read_only_fields = ['id', 'certificate_number', 'created_at']  # âœ… Added 'id' here
    
    def get_patient_name(self, obj):
        return obj.patient.pet_name if obj.patient else None
    
    def get_owner_name(self, obj):
        return obj.patient.owner.name if obj.patient and obj.patient.owner else None


# ============================================================================
# LAB TEST SERIALIZER
# ============================================================================

class LabTestSerializer(serializers.ModelSerializer):
    patient_name = serializers.SerializerMethodField()
    ordered_by_name = serializers.SerializerMethodField()
    
    class Meta:
        model = LabTest
        fields = [
            'id', 'patient', 'patient_name', 'medical_record',
            'test_name', 'test_type', 'ordered_date', 'sample_collected_date',
            'result_date', 'status', 'result_values', 'result_notes',
            'result_file', 'ordered_by', 'ordered_by_name', 'performed_by',
            'cost', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_patient_name(self, obj):
        return obj.patient.pet_name if obj.patient else None
    
    def get_ordered_by_name(self, obj):
        if obj.ordered_by:
            return obj.ordered_by.get_full_name() or obj.ordered_by.username
        return None


# ============================================================================
# SHARED URL SERIALIZER
# ============================================================================

class SharedURLSerializer(serializers.ModelSerializer):
    patient_name = serializers.SerializerMethodField()
    
    class Meta:
        model = SharedURL
        fields = [
            'id', 'patient', 'patient_name', 'share_type', 'short_code',
            'reference_id', 'created_at', 'expires_at', 'accessed_count',
            'last_accessed', 'ip_addresses'
        ]
        read_only_fields = ['id', 'short_code', 'created_at', 'accessed_count', 'last_accessed']
    
    def get_patient_name(self, obj):
        return obj.patient.pet_name if obj.patient else None


# ============================================================================
# PAYMENT SERIALIZER
# ============================================================================

class PaymentSerializer(serializers.ModelSerializer):
    patient_name = serializers.SerializerMethodField()
    medical_record_visit_date = serializers.SerializerMethodField()
    
    class Meta:
        model = Payment
        fields = [
            'id', 'patient', 'patient_name', 'medical_record', 
            'medical_record_visit_date', 'amount', 'payment_method', 
            'payment_status', 'transaction_id', 'consultation_fee',
            'medication_cost', 'lab_cost', 'other_charges', 'discount',
            'notes', 'payment_date', 'received_by', 'created_at'
        ]
        read_only_fields = ['created_at']
    
    def get_patient_name(self, obj):
        return obj.patient.pet_name if obj.patient else None
    
    def get_medical_record_visit_date(self, obj):
        if obj.medical_record:
            return obj.medical_record.visit_date
        return None


# ============================================================================
# SUBSCRIPTION SERIALIZER
# ============================================================================

class SubscriptionSerializer(serializers.ModelSerializer):
    user_email = serializers.SerializerMethodField()
    
    class Meta:
        model = Subscription
        fields = [
            'id', 'user', 'user_email', 'plan', 'is_active',
            'start_date', 'end_date', 'max_patients',
            'pdf_exports_limit', 'voice_transcriptions_limit',
            'current_pdf_exports', 'current_voice_uses',
            'last_reset', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_user_email(self, obj):
        return obj.user.email if obj.user else None


# ============================================================================
# AUDIT LOG SERIALIZER
# ============================================================================

class AuditLogSerializer(serializers.ModelSerializer):
    user_name = serializers.SerializerMethodField()
    
    class Meta:
        model = AuditLog
        fields = [
            'id', 'user', 'user_name', 'action', 'model_name',
            'object_id', 'description', 'ip_address', 'user_agent',
            'timestamp'
        ]
        read_only_fields = ['id', 'timestamp']
    
    def get_user_name(self, obj):
        if obj.user:
            return obj.user.get_full_name() or obj.user.username
        return None


# ============================================================================
# PASSBOOK SERIALIZERS
# ============================================================================
class PassbookSerializer(serializers.ModelSerializer):
    patient_id = serializers.UUIDField(write_only=True, required=False)
    
    # Add nested patient and owner info for display
    patient_name = serializers.CharField(source='patient.pet_name', read_only=True)
    patient_species = serializers.CharField(source='patient.species', read_only=True)
    patient_breed = serializers.CharField(source='patient.breed', read_only=True)
    patient_photo = serializers.SerializerMethodField()
    
    owner_name = serializers.CharField(source='patient.owner.name', read_only=True)
    owner_phone = serializers.CharField(source='patient.owner.phone', read_only=True)
    
    # Keep existing fields
    is_active = serializers.BooleanField(read_only=True)
    days_remaining = serializers.IntegerField(read_only=True)
    public_url = serializers.SerializerMethodField()
    
    class Meta:
        model = PetPassbook
        fields = [
            'id',
            'patient',
            'patient_id',
            'patient_name',
            'patient_species', 
            'patient_breed',
            'patient_photo',
            'owner_name',
            'owner_phone',
            'access_token',
            'is_enabled',
            'is_active',
            'subscription_start',
            'subscription_end',
            'subscription_type',
            'access_count',
            'days_remaining',
            'public_url',
            'created_at'
        ]
        read_only_fields = ['patient', 'access_token', 'is_active', 'created_at']
    
    def get_patient_photo(self, obj):
        """Get patient photo URL"""
        try:
            if obj.patient and obj.patient.photo:
                request = self.context.get('request')
                if request:
                    return request.build_absolute_uri(obj.patient.photo.url)
                return obj.patient.photo.url
        except Exception as e:
            print(f"Error getting patient photo: {e}")
        return None
    
    def get_public_url(self, obj):
        """Generate the public passbook URL"""
        request = self.context.get('request')
        if request:
            base_url = request.build_absolute_uri('/').rstrip('/')
            # Remove /api from base URL if present
            base_url = base_url.replace('/api', '')
            frontend_url = base_url.replace('dogger2-backend', 'dogger2-frontend')
            return f"{frontend_url}/passbook/public/{obj.access_token}"
        return f"/passbook/public/{obj.access_token}"
    
    def create(self, validated_data):
        patient_id = validated_data.pop('patient_id', None)
        
        if not patient_id:
            raise serializers.ValidationError("patient_id is required")
        
        try:
            patient = Patient.objects.get(id=patient_id)
        except Patient.DoesNotExist:
            raise serializers.ValidationError("Patient not found")
        
        # Check if passbook already exists
        passbook = PetPassbook.objects.filter(patient=patient).first()
        if passbook:
            return passbook
        
        # Create new passbook and auto-activate for 12 months
        passbook = PetPassbook.objects.create(patient=patient)
        passbook.activate_subscription(duration_months=12)
        
        return passbook

class PassbookPublicSerializer(serializers.Serializer):
    """Public passbook data (read-only, subscription-validated)"""
    
    # Clinic info
    clinic_name = serializers.SerializerMethodField()
    clinic_address = serializers.SerializerMethodField()
    
    # Pet info  
    pet_name = serializers.SerializerMethodField()
    species = serializers.SerializerMethodField()
    breed = serializers.SerializerMethodField()
    gender = serializers.SerializerMethodField()
    date_of_birth = serializers.SerializerMethodField()
    color = serializers.SerializerMethodField()
    photo = serializers.SerializerMethodField()
    
    # Owner info (limited)
    owner_name = serializers.SerializerMethodField()
    owner_phone = serializers.SerializerMethodField()
    
    # Medical data
    vaccinations = serializers.SerializerMethodField()
    consultations = serializers.SerializerMethodField()
    
    # Subscription status
    is_active = serializers.BooleanField(read_only=True)
    subscription_end = serializers.DateTimeField(read_only=True)
    days_remaining = serializers.IntegerField(read_only=True)
    
    def get_clinic_name(self, obj):
        return "Sri Adithya Pet Clinic"
    
    def get_clinic_address(self, obj):
        return "No:16,Sriram Nagar, Theni, Tamil Nadu - 625531"
    
    def get_pet_name(self, obj):
        try:
            return obj.patient.pet_name if obj.patient else "N/A"
        except Exception as e:
            print(f"Error getting pet_name: {e}")
            return "N/A"
    
    def get_species(self, obj):
        try:
            return obj.patient.species.title() if obj.patient else "N/A"
        except Exception as e:
            print(f"Error getting species: {e}")
            return "N/A"
    
    def get_breed(self, obj):
        try:
            return obj.patient.breed if obj.patient else "N/A"
        except Exception as e:
            print(f"Error getting breed: {e}")
            return "N/A"
    
    def get_gender(self, obj):
        try:
            return obj.patient.gender.title() if obj.patient else "N/A"
        except Exception as e:
            print(f"Error getting gender: {e}")
            return "N/A"
    
    def get_date_of_birth(self, obj):
        try:
            if obj.patient and obj.patient.date_of_birth:
                return obj.patient.date_of_birth.isoformat()
            return None
        except Exception as e:
            print(f"Error getting date_of_birth: {e}")
            return None
    
    def get_color(self, obj):
        try:
            return obj.patient.color if obj.patient else "N/A"
        except Exception as e:
            print(f"Error getting color: {e}")
            return "N/A"
    
    def get_photo(self, obj):
        """Get patient photo URL"""
        try:
            if obj.patient and obj.patient.photo:
                request = self.context.get('request')
                if request:
                    return request.build_absolute_uri(obj.patient.photo.url)
                return obj.patient.photo.url
        except Exception as e:
            print(f"Error getting photo: {e}")
        return None
    
    def get_owner_name(self, obj):
        try:
            if obj.patient and obj.patient.owner:
                return obj.patient.owner.name
        except Exception as e:
            print(f"Error getting owner_name: {e}")
        return "N/A"
    
    def get_owner_phone(self, obj):
        try:
            if obj.patient and obj.patient.owner:
                phone = obj.patient.owner.phone
                if phone and len(phone) > 4:
                    return phone[:4] + "****" + phone[-2:]
                return phone
        except Exception as e:
            print(f"Error getting owner_phone: {e}")
        return "N/A"
    
    def get_vaccinations(self, obj):
        if not obj.is_active:
            return []
        
        try:
            vaccinations = Vaccination.objects.filter(
                patient=obj.patient
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
    
    def get_consultations(self, obj):
        if not obj.is_active:
            return []
        
        try:
            records = MedicalRecord.objects.filter(
                patient=obj.patient
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