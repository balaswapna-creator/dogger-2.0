# backend/clinic/serializers.py
# ULTRA-COMPLETE VERSION - All possible serializers!

from rest_framework import serializers
from django.contrib.auth import get_user_model

# Import all models that might exist
try:
    from .models import (
        Patient, Owner, MedicalRecord, Vaccination, 
        Payment, Prescription
    )
except ImportError as e:
    print(f"Warning: Could not import some models: {e}")

# Try to import optional models
try:
    from .models import LabTest
except ImportError:
    LabTest = None

try:
    from .models import Passbook
except ImportError:
    Passbook = None

User = get_user_model()


# User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
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


class PaymentSerializer(serializers.ModelSerializer):
    patient_name = serializers.CharField(source='patient.name', read_only=True)
    
    class Meta:
        model = Payment
        fields = '__all__'


# Lab Test Serializer (if model exists)
if LabTest is not None:
    class LabTestSerializer(serializers.ModelSerializer):
        patient_name = serializers.CharField(source='patient.name', read_only=True)
        
        class Meta:
            model = LabTest
            fields = '__all__'
else:
    # Dummy serializer if LabTest doesn't exist
    class LabTestSerializer(serializers.Serializer):
        pass


# Passbook Serializer (if model exists)
if Passbook is not None:
    class PassbookSerializer(serializers.ModelSerializer):
        patient_name = serializers.CharField(source='patient.name', read_only=True)
        owner_name = serializers.CharField(source='patient.owner.name', read_only=True)
        
        class Meta:
            model = Passbook
            fields = '__all__'
else:
    # Dummy serializer if Passbook doesn't exist
    class PassbookSerializer(serializers.Serializer):
        pass


class PrescriptionSerializer(serializers.ModelSerializer):
    """
    Prescription serializer with multiple medicines support.
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
            'medicines',  # 🔥 CRITICAL!
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
        """Get patient name safely."""
        try:
            if obj.medical_record and obj.medical_record.patient:
                return obj.medical_record.patient.name
            return 'Unknown'
        except Exception as e:
            print(f"Error getting patient name: {e}")
            return 'Unknown'
    
    def get_medicine_count(self, obj):
        """Get medicine count."""
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
        🔥 CRITICAL: Ensures medicines is always returned as a list.
        """
        representation = super().to_representation(instance)
        
        # Ensure medicines is always a list
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
        
        print(f"📤 Prescription {instance.id}: {len(representation['medicines'])} medicines")
        
        return representation