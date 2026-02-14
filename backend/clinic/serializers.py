# backend/clinic/serializers.py
# ENHANCED VERSION - With comprehensive validation and error handling

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
        except Exception as e:
            print(f"Error getting patient name: {e}")
            return 'Unknown'
    
    def get_medicine_count(self, obj):
        try:
            if obj.medicines and isinstance(obj.medicines, list):
                return len(obj.medicines)
            if obj.medication_name:
                return 1
            return 0
        except Exception as e:
            print(f"Error getting medicine count: {e}")
            return 0


class PrescriptionSerializer(serializers.ModelSerializer):
    """
    Full prescription serializer with comprehensive validation.
    🔥 ENHANCED: Implements all validation from the ideas document
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
        🔥 ENHANCED: Comprehensive medical record validation
        Prevents null medical records and ensures patient is assigned
        """
        if not value:
            raise serializers.ValidationError(
                "Medical record is required. Please select a consultation before creating a prescription."
            )
        
        # Check if medical record exists in database
        try:
            medical_record = MedicalRecord.objects.get(id=value.id)
        except MedicalRecord.DoesNotExist:
            raise serializers.ValidationError(
                f"Invalid medical record ID. The selected consultation does not exist."
            )
        
        # Check if medical record has a patient assigned
        if not hasattr(medical_record, 'patient') or not medical_record.patient:
            raise serializers.ValidationError(
                f"The selected consultation (ID: {value.id}) does not have a patient assigned. "
                "Please assign a patient to the medical record first."
            )
        
        # Additional validation: Check if patient still exists
        try:
            patient = medical_record.patient
            if not patient.pet_name:
                raise serializers.ValidationError(
                    "The patient associated with this consultation has no name. Please update the patient record."
                )
        except Exception as e:
            raise serializers.ValidationError(
                f"Error accessing patient information: {str(e)}"
            )
        
        return value
    
    def validate_medicines(self, value):
        """
        🔥 ENHANCED: Comprehensive medicines array validation
        Implements all checks from the ideas document
        """
        # Allow None, will be checked in overall validate()
        if value is None:
            return value
        
        # Check if it's a list
        if not isinstance(value, list):
            raise serializers.ValidationError(
                "Medicines must be provided as an array/list. "
                f"Received type: {type(value).__name__}"
            )
        
        # Check if array is empty
        if len(value) == 0:
            raise serializers.ValidationError(
                "At least one medicine is required. Please add medicines to the prescription."
            )
        
        # Validate each medicine in the array
        required_fields = ['medication_name', 'dosage', 'frequency', 'duration']
        
        for index, medicine in enumerate(value):
            medicine_position = index + 1
            
            # Check if medicine is a dictionary/object
            if not isinstance(medicine, dict):
                raise serializers.ValidationError(
                    f"Medicine #{medicine_position} must be an object with fields. "
                    f"Received type: {type(medicine).__name__}"
                )
            
            # Check each required field
            missing_fields = []
            empty_fields = []
            
            for field in required_fields:
                # Check if field exists
                if field not in medicine:
                    missing_fields.append(field)
                # Check if field has a value (not None, not empty string)
                elif not medicine[field] or not str(medicine[field]).strip():
                    empty_fields.append(field)
            
            # Report missing fields
            if missing_fields:
                raise serializers.ValidationError(
                    f"Medicine #{medicine_position} is missing required fields: {', '.join(missing_fields)}. "
                    "All medicines must have: medication_name, dosage, frequency, and duration."
                )
            
            # Report empty fields
            if empty_fields:
                raise serializers.ValidationError(
                    f"Medicine #{medicine_position} has empty required fields: {', '.join(empty_fields)}. "
                    "Please fill in all required fields."
                )
            
            # Validate medication_name specifically (common error)
            if len(str(medicine['medication_name']).strip()) < 2:
                raise serializers.ValidationError(
                    f"Medicine #{medicine_position}: Medication name must be at least 2 characters long."
                )
            
            # Optional: Validate dosage format (can be customized)
            dosage = str(medicine['dosage']).strip()
            if len(dosage) < 1:
                raise serializers.ValidationError(
                    f"Medicine #{medicine_position}: Dosage cannot be empty."
                )
        
        return value
    
    def validate(self, data):
        """
        🔥 ENHANCED: Overall validation
        Ensures at least one medicine method is used and data consistency
        """
        medicines = data.get('medicines')
        medication_name = data.get('medication_name')
        
        # Check if using new medicines array or old single-medicine fields
        has_medicines_array = medicines and isinstance(medicines, list) and len(medicines) > 0
        has_single_medicine = medication_name and str(medication_name).strip()
        
        # Must have at least one medicine method
        if not has_medicines_array and not has_single_medicine:
            raise serializers.ValidationError({
                'medicines': [
                    'Please add at least one medicine to the prescription.',
                    'Either provide a medicines array or fill in the single medicine fields.'
                ]
            })
        
        # If using old format, validate those fields too
        if has_single_medicine and not has_medicines_array:
            if not data.get('dosage'):
                raise serializers.ValidationError({
                    'dosage': 'Dosage is required when using single medicine format.'
                })
            if not data.get('frequency'):
                raise serializers.ValidationError({
                    'frequency': 'Frequency is required when using single medicine format.'
                })
            if not data.get('duration'):
                raise serializers.ValidationError({
                    'duration': 'Duration is required when using single medicine format.'
                })
        
        return data
    
    def get_patient_name(self, obj):
        """
        🔥 ENHANCED: Safe patient name retrieval with detailed error logging
        """
        try:
            if not obj.medical_record:
                print(f"⚠️ Prescription {obj.id}: No medical record assigned")
                return 'No Medical Record'
            
            if not obj.medical_record.patient:
                print(f"⚠️ Prescription {obj.id}: Medical record has no patient")
                return 'No Patient Assigned'
            
            patient_name = obj.medical_record.patient.pet_name
            if not patient_name:
                print(f"⚠️ Prescription {obj.id}: Patient has no name")
                return 'Unnamed Patient'
            
            return patient_name
            
        except Exception as e:
            print(f"❌ Error getting patient name for prescription {obj.id}: {e}")
            import traceback
            traceback.print_exc()
            return 'Error'
    
    def get_medicine_count(self, obj):
        """
        Get count of medicines with error handling
        """
        try:
            if obj.medicines and isinstance(obj.medicines, list):
                return len(obj.medicines)
            if obj.medication_name:
                return 1
            return 0
        except Exception as e:
            print(f"❌ Error getting medicine count for prescription {obj.id}: {e}")
            return 0
    
    def to_representation(self, instance):
        """
        🔥 ENHANCED: Ensure medicines is ALWAYS a proper list
        Also adds helpful debug information
        """
        representation = super().to_representation(instance)
        
        # Get the medicines field
        medicines = representation.get('medicines')
        
        # Ensure it's always a list
        if medicines is None:
            print(f"ℹ️ Prescription {instance.id}: medicines is None, setting to empty list")
            representation['medicines'] = []
        elif isinstance(medicines, str):
            # Try to parse JSON string
            try:
                import json
                representation['medicines'] = json.loads(medicines)
                print(f"ℹ️ Prescription {instance.id}: Parsed medicines from JSON string")
            except Exception as e:
                print(f"❌ Prescription {instance.id}: Failed to parse medicines string: {e}")
                representation['medicines'] = []
        elif not isinstance(medicines, list):
            print(f"⚠️ Prescription {instance.id}: medicines is {type(medicines).__name__}, converting to list")
            representation['medicines'] = []
        
        # Add debug info in development
        if representation['medicines']:
            print(f"✅ Prescription {instance.id}: Returning {len(representation['medicines'])} medicine(s)")
        
        return representation
    
    def create(self, validated_data):
        """
        🔥 ENHANCED: Custom create method with logging
        """
        try:
            print(f"📝 Creating prescription with data: {validated_data.keys()}")
            instance = super().create(validated_data)
            print(f"✅ Successfully created prescription {instance.id}")
            return instance
        except Exception as e:
            print(f"❌ Error creating prescription: {e}")
            import traceback
            traceback.print_exc()
            raise
    
    def update(self, instance, validated_data):
        """
        🔥 ENHANCED: Custom update method with logging
        """
        try:
            print(f"📝 Updating prescription {instance.id} with data: {validated_data.keys()}")
            instance = super().update(instance, validated_data)
            print(f"✅ Successfully updated prescription {instance.id}")
            return instance
        except Exception as e:
            print(f"❌ Error updating prescription {instance.id}: {e}")
            import traceback
            traceback.print_exc()
            raise