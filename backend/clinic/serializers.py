# backend/clinic/serializers.py
# COMPLETE VERSION - All serializers included!

from rest_framework import serializers
from .models import Patient, Owner, MedicalRecord, Vaccination, Payment, Prescription, LabTest


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


class LabTestSerializer(serializers.ModelSerializer):
    """Lab Test serializer."""
    patient_name = serializers.CharField(source='patient.name', read_only=True)
    
    class Meta:
        model = LabTest
        fields = '__all__'


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
        except:
            return 'Unknown'
    
    def get_medicine_count(self, obj):
        """Get medicine count."""
        try:
            if obj.medicines and isinstance(obj.medicines, list):
                return len(obj.medicines)
            if obj.medication_name:
                return 1
            return 0
        except:
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