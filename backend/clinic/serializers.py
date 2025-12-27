from rest_framework import serializers
from .models import (
    User, Owner, Patient, MedicalRecord, Prescription,
    Vaccination, LabTest, SharedURL, Payment, Subscription, AuditLog
)
from rest_framework import serializers
from .models import PetPassbook, Patient, Owner, MedicalRecord, Vaccination, Prescription
from rest_framework import serializers
from .models import Passbook, Prescription

class PassbookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Passbook
        fields = '__all__'

class PrescriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Prescription
        fields = '__all__'


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
    class Meta:
        model = Owner
        fields = [
            'id', 'name', 'phone', 'email', 'address', 
            'city', 'whatsapp_number', 'created_at', 'updated_at', 'created_by'
        ]
        read_only_fields = ['created_at', 'updated_at']


# ============================================================================
# PATIENT SERIALIZER
# ============================================================================

class PatientSerializer(serializers.ModelSerializer):
    owner_name = serializers.SerializerMethodField()
    
    class Meta:
        model = Patient
        fields = [
            'id', 'pet_name', 'species', 'breed', 'gender', 
            'date_of_birth', 'color', 'microchip_id', 'photo', 
            'owner', 'owner_name', 'qr_code', 'allergies', 
            'chronic_conditions', 'current_medications', 'is_active',
            'last_visit', 'created_at', 'updated_at', 'created_by'
        ]
        read_only_fields = ['created_at', 'updated_at', 'qr_code']
    
    def get_owner_name(self, obj):
        return obj.owner.name if obj.owner else "No Owner"


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

class PrescriptionSerializer(serializers.ModelSerializer):
    patient_name = serializers.SerializerMethodField()
    doctor_name = serializers.SerializerMethodField()
    
    class Meta:
        model = Prescription
        fields = [
            'id', 'medical_record', 
            'medication_name', 'dosage', 'frequency', 'duration', 
            'instructions', 'quantity', 'price',
            'patient_name', 'doctor_name',
            'created_at'
        ]
        read_only_fields = ['created_at']
    
    def get_patient_name(self, obj):
        if obj.medical_record and obj.medical_record.patient:
            return obj.medical_record.patient.pet_name
        return None
    
    def get_doctor_name(self, obj):
        if obj.medical_record and obj.medical_record.doctor:
            return obj.medical_record.doctor.get_full_name()
        return None


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
        read_only_fields = ['certificate_number', 'created_at']
    
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

# ============================================
# FILE: backend/clinic/serializers.py (ADD THIS)
# ============================================

class PassbookSerializer(serializers.ModelSerializer):
    patient_name = serializers.CharField(source='patient.pet_name', read_only=True)
    is_active = serializers.BooleanField(read_only=True)
    days_remaining = serializers.IntegerField(read_only=True)
    qr_url = serializers.SerializerMethodField()
    
    class Meta:
        model = PetPassbook
        fields = [
            'id', 'patient', 'patient_name', 'access_token', 
            'is_enabled', 'is_active', 'subscription_start', 
            'subscription_end', 'subscription_type', 'days_remaining',
            'qr_url', 'access_count', 'last_accessed'
        ]
        read_only_fields = ['id', 'access_token', 'access_count', 'last_accessed']
    
    def get_qr_url(self, obj):
        request = self.context.get('request')
        if request:
            return f"{request.scheme}://{request.get_host()}/passbook/{obj.access_token}"
        return f"/passbook/{obj.access_token}"


class PassbookPublicSerializer(serializers.Serializer):
    """Public passbook data (read-only, subscription-validated)"""
    
    # Clinic info
    clinic_name = serializers.SerializerMethodField()
    clinic_address = serializers.SerializerMethodField()
    
    # Pet info
    pet_name = serializers.CharField(source='patient.pet_name')
    species = serializers.CharField(source='patient.species')
    breed = serializers.CharField(source='patient.breed')
    gender = serializers.CharField(source='patient.gender')
    date_of_birth = serializers.DateField(source='patient.date_of_birth')
    color = serializers.CharField(source='patient.color')
    photo = serializers.ImageField(source='patient.photo')
    
    # Owner info (limited)
    owner_name = serializers.SerializerMethodField()
    owner_phone = serializers.SerializerMethodField()
    
    # Medical data (only if active subscription)
    vaccinations = serializers.SerializerMethodField()
    consultations = serializers.SerializerMethodField()
    
    # Subscription status
    is_active = serializers.BooleanField()
    subscription_end = serializers.DateTimeField()
    days_remaining = serializers.IntegerField()
    
    def get_clinic_name(self, obj):
        return "Sri Adithya Pet Clinic"
    
    def get_clinic_address(self, obj):
        return "Main Road, Cumbum, Tamil Nadu - 625516"
    
    def get_owner_name(self, obj):
        try:
            owner = Owner.objects.get(id=obj.patient.owner_id)
            return owner.name
        except Owner.DoesNotExist:
            return "N/A"
    
    def get_owner_phone(self, obj):
        try:
            owner = Owner.objects.get(id=obj.patient.owner_id)
            # Mask phone number for privacy
            phone = owner.phone
            if len(phone) > 4:
                return phone[:4] + "****" + phone[-2:]
            return phone
        except Owner.DoesNotExist:
            return "N/A"
    
    def get_vaccinations(self, obj):
        if not obj.is_active:
            return []
        
        vaccinations = Vaccination.objects.filter(patient=obj.patient).order_by('-date_administered')[:10]
        return [{
            'vaccine_name': v.vaccine_name,
            'date_administered': v.date_administered,
            'next_due_date': v.next_due_date,
            'certificate_number': v.certificate_number,
            'administered_by': v.administered_by or 'Dr. A. Balasubramanian'
        } for v in vaccinations]
    
    def get_consultations(self, obj):
        if not obj.is_active:
            return []
        
        records = MedicalRecord.objects.filter(patient=obj.patient).order_by('-visit_date')[:10]
        return [{
            'visit_date': r.visit_date,
            'visit_type': r.visit_type,
            'chief_complaint': r.chief_complaint,
            'diagnosis': r.diagnosis,
            'treatment_plan': r.treatment_plan,
            'temperature': r.temperature,
            'weight': r.weight
        } for r in records]
