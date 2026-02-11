# backend/clinic/serializers.py
# CLEAN VERSION - Fixed and validated

from rest_framework import serializers
from django.contrib.auth import get_user_model

# Import all models
try:
    from .models import (
        Patient, Owner, MedicalRecord, Vaccination, 
        Payment, Prescription, LabTest, Passbook
    )
except ImportError as e:
    print(f"Warning: Could not import some models: {e}")
    # Set to None if not found
    LabTest = None
    Passbook = None

User = get_user_model()


# ==================== USER SERIALIZER ====================
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
        read_only_fields = ['id']


# ==================== OWNER SERIALIZER ====================
class OwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Owner
        fields = '__all__'


# ==================== PATIENT SERIALIZER ====================
class PatientSerializer(serializers.ModelSerializer):
    owner_name = serializers.CharField(source='owner.name', read_only=True)
    
    class Meta:
        model = Patient
        fields = '__all__'


# ==================== MEDICAL RECORD SERIALIZER ====================
class MedicalRecordSerializer(serializers.ModelSerializer):
    patient_name = serializers.CharField(source='patient.pet_name', read_only=True)
    
    class Meta:
        model = MedicalRecord
        fields = '__all__'
    
    def validate_patient(self, value):
        """Ensure patient is provided for medical records"""
        if not value:
            raise serializers.ValidationError(
                "Patient is required for medical records"
            )
        return value


# ==================== VACCINATION SERIALIZER ====================
class VaccinationSerializer(serializers.ModelSerializer):
    patient_name = serializers.CharField(source='patient.pet_name', read_only=True)
    
    class Meta:
        model = Vaccination
        fields = '__all__'


# ==================== PAYMENT SERIALIZER ====================
class PaymentSerializer(serializers.ModelSerializer):
    patient_name = serializers.CharField(source='patient.pet_name', read_only=True)
    
    class Meta:
        model = Payment
        fields = '__all__'


# ==================== LAB TEST SERIALIZER ====================
if LabTest is not None:
    class LabTestSerializer(serializers.ModelSerializer):
        patient_name = serializers.CharField(source='patient.pet_name', read_only=True)
        
        class Meta:
            model = LabTest
            fields = '__all__'
else:
    class LabTestSerializer(serializers.Serializer):
        pass


# ==================== PASSBOOK SERIALIZERS ====================
if Passbook is not None:
    class PassbookSerializer(serializers.ModelSerializer):
        patient_name = serializers.CharField(source='patient.pet_name', read_only=True)
        owner_name = serializers.CharField(source='patient.owner.name', read_only=True)
        
        class Meta:
            model = Passbook
            fields = '__all__'
    
    # Public version (for public viewing without authentication)
    class PassbookPublicSerializer(serializers.ModelSerializer):
        patient_name = serializers.CharField(source='patient.pet_name', read_only=True)
        owner_name = serializers.CharField(source='patient.owner.name', read_only=True)
        patient_details = serializers.SerializerMethodField()
        owner_details = serializers.SerializerMethodField()
        
        class Meta:
            model = Passbook
            fields = [
                'id', 'patient', 'patient_name', 'owner_name',
                'patient_details', 'owner_details', 'qr_code',
                'created_at', 'is_active'
            ]
        
        def get_patient_details(self, obj):
            if obj.patient:
                return {
                    'name': obj.patient.pet_name,
                    'species': obj.patient.species,
                    'breed': obj.patient.breed,
                    'age': obj.patient.age,
                }
            return None
        
        def get_owner_details(self, obj):
            if obj.patient and obj.patient.owner:
                return {
                    'name': obj.patient.owner.name,
                    'phone': obj.patient.owner.phone,
                    'address': obj.patient.owner.address,
                }
            return None
else:
    class PassbookSerializer(serializers.Serializer):
        pass
    
    class PassbookPublicSerializer(serializers.Serializer):
        pass


# ==================== PRESCRIPTION SERIALIZERS ====================

class PrescriptionListSerializer(serializers.ModelSerializer):
    """
    Lightweight serializer for listing prescriptions.
    """
    patient_name = serializers.SerializerMethodField()
    medicine_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Prescription
        fields = [
            'id',
            'medical_record',
            'patient_name',
            'medicine_count',
            'created_at',
        ]
        read_only_fields = ['id', 'created_at', 'patient_name', 'medicine_count']
    
    def get_patient_name(self, obj):
        try:
            if obj.medical_record and obj.medical_record.patient:
                return obj.medical_record.patient.pet_name
            return 'Unknown'
        except:
            return 'Unknown'
    
    def get_medicine_count(self, obj):
        try:
            if obj.medicines and isinstance(obj.medicines, list):
                return len(obj.medicines)
            if obj.medication_name:
                return 1
            return 0
        except:
            return 0


class PrescriptionSerializer(serializers.ModelSerializer):
    """
    Full prescription serializer with validation and multiple medicines support.
    """
    patient_name = serializers.SerializerMethodField()
    medicine_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Prescription
        fields = [
            'id',
            'medical_record',
            'patient_name',
            'medicine_count',
            'medicines',
            'created_at',
            'updated_at',
            # Old single-medicine fields (backward compatibility)
            'medication_name',
            'dosage',
            'frequency',
            'duration',
            'instructions',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'patient_name', 'medicine_count']
    
    def validate_medical_record(self, value):
        """
        Validate that medical_record is provided and has a patient
        """
        if not value:
            raise serializers.ValidationError(
                "Medical record is required. Please select a consultation before creating a prescription."
            )
        
        # Check if medical record has a patient
        if not hasattr(value, 'patient') or not value.patient:
            raise serializers.ValidationError(
                f"The selected medical record does not have a patient assigned. "
                "Please assign a patient to the medical record first."
            )
        
        return value
    
    def validate_medicines(self, value):
        """
        Validate medicines array structure and content
        """
        if value is None:
            # Allow None, will check in overall validate()
            return value
            
        if not isinstance(value, list):
            raise serializers.ValidationError(
                "Medicines must be a list/array"
            )
        
        if len(value) == 0:
            raise serializers.ValidationError(
                "Medicines array cannot be empty. Please add at least one medicine."
            )
        
        # Validate each medicine has required fields
        required_fields = ['medication_name', 'dosage', 'frequency', 'duration']
        
        for index, medicine in enumerate(value):
            if not isinstance(medicine, dict):
                raise serializers.ValidationError(
                    f"Medicine at position {index + 1} must be an object with fields"
                )
            
            # Check required fields
            missing_fields = []
            for field in required_fields:
                if field not in medicine or not medicine[field] or not str(medicine[field]).strip():
                    missing_fields.append(field)
            
            if missing_fields:
                raise serializers.ValidationError(
                    f"Medicine at position {index + 1} is missing required fields: {', '.join(missing_fields)}"
                )
        
        return value
    
    def validate(self, data):
        """
        Overall validation - ensure at least one medicine method is used
        """
        medicines = data.get('medicines')
        medication_name = data.get('medication_name')
        
        # Check if using new medicines array or old single-medicine fields
        has_medicines_array = medicines and isinstance(medicines, list) and len(medicines) > 0
        has_single_medicine = medication_name and medication_name.strip()
        
        if not has_medicines_array and not has_single_medicine:
            raise serializers.ValidationError({
                'medicines': 'Please add at least one medicine to the prescription'
            })
        
        return data
    
    def get_patient_name(self, obj):
        """
        Get patient name safely with proper error handling
        """
        try:
            if not obj.medical_record:
                return 'No Medical Record'
            
            if not obj.medical_record.patient:
                return 'No Patient Assigned'
            
            return obj.medical_record.patient.pet_name
        except Exception as e:
            print(f"Error getting patient name: {e}")
            return 'Error'
    
    def get_medicine_count(self, obj):
        """
        Get count of medicines
        """
        try:
            if obj.medicines and isinstance(obj.medicines, list):
                return len(obj.medicines)
            if obj.medication_name:
                return 1
            return 0
        except Exception as e:
            print(f"Error getting medicine count: {e}")
            return 0
    
    def to_representation(self, instance):
        """
        Ensure medicines is ALWAYS returned as a proper list (never undefined)
        """
        representation = super().to_representation(instance)
        
        # Get the medicines field
        medicines = representation.get('medicines')
        
        # Ensure it's always a list
        if medicines is None:
            representation['medicines'] = []
        elif isinstance(medicines, str):
            # If it's a string, try to parse it
            try:
                import json
                representation['medicines'] = json.loads(medicines)
            except Exception as e:
                print(f"Failed to parse medicines string: {e}")
                representation['medicines'] = []
        elif not isinstance(medicines, list):
            print(f"Warning: medicines is type {type(medicines)}, converting to list")
            representation['medicines'] = []
        
        return representation