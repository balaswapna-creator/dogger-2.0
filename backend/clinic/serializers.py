# backend/clinic/serializers.py
# HEAVILY DEBUGGED VERSION - Shows exactly what's happening

from rest_framework import serializers
from .models import Patient, Owner, MedicalRecord, Vaccination, Payment, Prescription


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


class PrescriptionSerializer(serializers.ModelSerializer):
    """
    Prescription serializer with HEAVY debugging.
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
            'medicines',  # 🔥 THIS MUST BE HERE!
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
        """Get patient name with HEAVY debugging."""
        print(f"🔍 Getting patient name for prescription {obj.id}")
        
        try:
            # Check if medical_record exists
            if not obj.medical_record:
                print(f"❌ No medical_record on prescription {obj.id}")
                return 'Unknown'
            
            print(f"✅ Medical record exists: {obj.medical_record.id}")
            
            # Check if medical_record has patient
            if not obj.medical_record.patient:
                print(f"❌ Medical record {obj.medical_record.id} has no patient")
                return 'Unknown'
            
            print(f"✅ Patient exists: {obj.medical_record.patient.id}")
            
            # Get patient name
            patient_name = obj.medical_record.patient.name
            print(f"✅ Patient name: {patient_name}")
            
            return patient_name
            
        except Exception as e:
            print(f"❌ Error getting patient name: {type(e).__name__}: {e}")
            return 'Unknown'
    
    def get_medicine_count(self, obj):
        """Get medicine count with debugging."""
        print(f"🔍 Getting medicine count for prescription {obj.id}")
        
        try:
            # Check medicines field
            print(f"   medicines type: {type(obj.medicines)}")
            print(f"   medicines value: {obj.medicines}")
            
            if obj.medicines and isinstance(obj.medicines, list):
                count = len(obj.medicines)
                print(f"✅ Medicine count from medicines array: {count}")
                return count
            
            if obj.medication_name:
                print(f"✅ Medicine count from old format: 1")
                return 1
            
            print(f"⚠️ No medicines found, returning 0")
            return 0
            
        except Exception as e:
            print(f"❌ Error getting medicine count: {type(e).__name__}: {e}")
            return 0
    
    def to_representation(self, instance):
        """
        🔥 CRITICAL: Convert to JSON response with HEAVY debugging.
        """
        print(f"\n{'='*60}")
        print(f"📤 SERIALIZING PRESCRIPTION {instance.id}")
        print(f"{'='*60}")
        
        # Call parent method
        representation = super().to_representation(instance)
        
        print(f"Initial representation keys: {representation.keys()}")
        
        # Check medicines field
        medicines = representation.get('medicines')
        print(f"Medicines from representation: {medicines}")
        print(f"Medicines type: {type(medicines)}")
        
        # Also check directly from instance
        print(f"Direct from instance.medicines: {instance.medicines}")
        print(f"Direct type: {type(instance.medicines)}")
        
        # Ensure it's always a list
        if medicines is None:
            print(f"⚠️ medicines is None, setting to []")
            representation['medicines'] = []
        elif isinstance(medicines, str):
            print(f"⚠️ medicines is string, parsing: {medicines}")
            try:
                import json
                representation['medicines'] = json.loads(medicines)
                print(f"✅ Parsed to: {representation['medicines']}")
            except Exception as e:
                print(f"❌ Failed to parse: {e}")
                representation['medicines'] = []
        elif not isinstance(medicines, list):
            print(f"⚠️ medicines is not list (type: {type(medicines)}), setting to []")
            representation['medicines'] = []
        else:
            print(f"✅ medicines is already a list with {len(medicines)} items")
        
        print(f"FINAL medicines value: {representation['medicines']}")
        print(f"FINAL representation: {representation}")
        print(f"{'='*60}\n")
        
        return representation