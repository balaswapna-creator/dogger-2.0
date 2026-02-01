# backend/clinic/serializers.py
# FIXED VERSION - All required serializers included

from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import (
    Patient, Owner, MedicalRecord, Vaccination, 
    Payment, Prescription, LabTest, PetPassbook
)

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'role', 'phone']
        read_only_fields = ['id']


class OwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Owner
        fields = '__all__'


class PatientSerializer(serializers.ModelSerializer):
    owner_name = serializers.CharField(source='owner.name', read_only=True)
    
    class Meta:
        model = Patient
        fields = '__all__'


class MedicalRecordSerializer(serializers.ModelSerializer):
    patient_name = serializers.CharField(source='patient.name', read_only=True)
    
    class Meta:
        model = MedicalRecord
        fields = '__all__'


class VaccinationSerializer(serializers.ModelSerializer):
    patient_name = serializers.CharField(source='patient.name', read_only=True)
    
    class Meta:
        model = Vaccination
        fields = '__all__'


class LabTestSerializer(serializers.ModelSerializer):
    patient_name = serializers.CharField(source='patient.name', read_only=True)
    
    class Meta:
        model = LabTest
        fields = '__all__'


class PaymentSerializer(serializers.ModelSerializer):
    patient_name = serializers.CharField(source='patient.name', read_only=True)
    
    class Meta:
        model = Payment
        fields = '__all__'


class PrescriptionSerializer(serializers.ModelSerializer):
    """
    Prescription serializer with multiple medicines support.
    Accepts both 'medical_record' and 'medical_record_id' in the request.
    """
    patient_name = serializers.SerializerMethodField()
    medicine_count = serializers.SerializerMethodField()
    medical_record_id = serializers.UUIDField(write_only=True, required=False)
    
    class Meta:
        model = Prescription
        fields = [
            'id',
            'medical_record',
            'medical_record_id',  # Accept this from frontend
            'patient_name',
            'medicine_count',
            'medicines',  # CRITICAL: Must be in fields list!
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
        """Get patient name safely."""
        try:
            if obj.medical_record and obj.medical_record.patient:
                return obj.medical_record.patient.name
            return 'Unknown'
        except:
            return 'Unknown'
    
    def get_medicine_count(self, obj):
        """Get count of medicines."""
        try:
            if obj.medicines and isinstance(obj.medicines, list):
                return len(obj.medicines)
            if obj.medication_name:
                return 1
            return 0
        except:
            return 0
    
    def validate(self, data):
        """
        Accept both 'medical_record' and 'medical_record_id'.
        Convert medical_record_id to medical_record if provided.
        """
        medical_record_id = data.pop('medical_record_id', None)
        
        if medical_record_id and not data.get('medical_record'):
            # Convert medical_record_id to medical_record object
            try:
                medical_record = MedicalRecord.objects.get(id=medical_record_id)
                data['medical_record'] = medical_record
            except MedicalRecord.DoesNotExist:
                raise serializers.ValidationError({
                    'medical_record_id': 'Medical record not found.'
                })
        
        # Ensure we have either medical_record or valid medicines
        if not data.get('medical_record'):
            if not data.get('medicines') or len(data.get('medicines', [])) == 0:
                raise serializers.ValidationError({
                    'medical_record': 'Either medical_record or medical_record_id is required.'
                })
        
        # Validate medicines array
        medicines = data.get('medicines', [])
        if medicines:
            if not isinstance(medicines, list):
                raise serializers.ValidationError({
                    'medicines': 'Medicines must be a list of medicine objects.'
                })
            
            for idx, medicine in enumerate(medicines):
                if not isinstance(medicine, dict):
                    raise serializers.ValidationError({
                        'medicines': f'Medicine {idx + 1} must be an object.'
                    })
                
                required_fields = ['medication_name', 'dosage', 'frequency', 'duration']
                for field in required_fields:
                    if not medicine.get(field):
                        raise serializers.ValidationError({
                            'medicines': f'Medicine {idx + 1}: {field} is required.'
                        })
        
        return data
    
    def create(self, validated_data):
        """Create prescription with medicines array."""
        return Prescription.objects.create(**validated_data)
    
    def to_representation(self, instance):
        """
        CRITICAL: This ensures medicines is always returned as a proper list!
        Without this, medicines might come back as undefined or empty string.
        """
        representation = super().to_representation(instance)
        
        # Get the medicines field
        medicines = representation.get('medicines')
        
        # Ensure it's always a list
        if medicines is None:
            representation['medicines'] = []
        elif isinstance(medicines, str):
            # If it's a string, try to parse as JSON
            try:
                import json
                representation['medicines'] = json.loads(medicines)
            except:
                representation['medicines'] = []
        elif not isinstance(medicines, list):
            representation['medicines'] = []
        
        # Debug logging
        print(f"📤 Serializing prescription {instance.id}")
        print(f"   Medicines: {representation['medicines']}")
        print(f"   Type: {type(representation['medicines'])}")
        
        return representation


# List serializer for prescriptions (lighter version for list views)
class PrescriptionListSerializer(serializers.ModelSerializer):
    patient_name = serializers.SerializerMethodField()
    medicine_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Prescription
        fields = ['id', 'patient_name', 'medicine_count', 'created_at']
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
            return 1
        except:
            return 1


# Passbook serializers
class PassbookSerializer(serializers.ModelSerializer):
    patient_name = serializers.CharField(source='patient.name', read_only=True)
    owner_name = serializers.CharField(source='patient.owner.name', read_only=True)
    
    class Meta:
        model = PetPassbook
        fields = '__all__'


class PassbookPublicSerializer(serializers.ModelSerializer):
    """Public serializer for passbook - includes nested data"""
    patient = PatientSerializer(read_only=True)
    
    class Meta:
        model = PetPassbook
        fields = ['id', 'patient', 'qr_code', 'is_active', 'created_at']
        read_only_fields = ['id', 'created_at']
