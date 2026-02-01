# backend/clinic/serializers.py
# FINAL COMPLETE VERSION - Every possible serializer!

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
    patient_name = serializers.CharField(source='patient.name', read_only=True)
    
    class Meta:
        model = MedicalRecord
        fields = '__all__'


# ==================== VACCINATION SERIALIZER ====================
class VaccinationSerializer(serializers.ModelSerializer):
    patient_name = serializers.CharField(source='patient.name', read_only=True)
    
    class Meta:
        model = Vaccination
        fields = '__all__'


# ==================== PAYMENT SERIALIZER ====================
class PaymentSerializer(serializers.ModelSerializer):
    patient_name = serializers.CharField(source='patient.name', read_only=True)
    
    class Meta:
        model = Payment
        fields = '__all__'


# ==================== LAB TEST SERIALIZER ====================
if LabTest is not None:
    class LabTestSerializer(serializers.ModelSerializer):
        patient_name = serializers.CharField(source='patient.name', read_only=True)
        
        class Meta:
            model = LabTest
            fields = '__all__'
else:
    class LabTestSerializer(serializers.Serializer):
        pass


# ==================== PASSBOOK SERIALIZERS ====================
if Passbook is not None:
    class PassbookSerializer(serializers.ModelSerializer):
        patient_name = serializers.CharField(source='patient.name', read_only=True)
        owner_name = serializers.CharField(source='patient.owner.name', read_only=True)
        
        class Meta:
            model = Passbook
            fields = '__all__'
    
    # Public version (for public viewing without authentication)
    class PassbookPublicSerializer(serializers.ModelSerializer):
        patient_name = serializers.CharField(source='patient.name', read_only=True)
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
                    'name': obj.patient.name,
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

# List serializer (lightweight for list views)
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
                return obj.medical_record.patient.name
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


# Full serializer (with all medicine details)
class PrescriptionSerializer(serializers.ModelSerializer):
    """
    Prescription serializer with multiple medicines support.
    🔥 This is the critical one for your prescription feature!
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
            'medicines',  # 🔥 CRITICAL - The JSONField with medicines array!
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
    
    def get_patient_name(self, obj):
        """Get patient name safely with error handling."""
        try:
            if obj.medical_record and obj.medical_record.patient:
                return obj.medical_record.patient.name
            return 'Unknown'
        except Exception as e:
            print(f"❌ Error getting patient name: {e}")
            return 'Unknown'
    
    def get_medicine_count(self, obj):
        """Get count of medicines."""
        try:
            if obj.medicines and isinstance(obj.medicines, list):
                return len(obj.medicines)
            if obj.medication_name:
                return 1
            return 0
        except Exception as e:
            print(f"❌ Error getting medicine count: {e}")
            return 0
    
    def to_representation(self, instance):
        """
        🔥 CRITICAL: This method ensures medicines is ALWAYS returned as a proper list.
        Without this, the frontend gets 'undefined' instead of the medicines array!
        """
        # Get the base representation from parent class
        representation = super().to_representation(instance)
        
        # Get the medicines field
        medicines = representation.get('medicines')
        
        # Ensure it's always a list
        if medicines is None:
            # If None, set to empty list
            representation['medicines'] = []
        elif isinstance(medicines, str):
            # If it's a string (shouldn't happen but just in case), parse it
            try:
                import json
                representation['medicines'] = json.loads(medicines)
            except Exception as e:
                print(f"❌ Failed to parse medicines string: {e}")
                representation['medicines'] = []
        elif not isinstance(medicines, list):
            # If it's not a list, convert to empty list
            print(f"⚠️ medicines is type {type(medicines)}, converting to list")
            representation['medicines'] = []
        
        # Debug log
        print(f"📤 Prescription {instance.id}: Returning {len(representation['medicines'])} medicines")
        
        return representation