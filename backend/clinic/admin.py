"""
Clinic App Admin Configuration
✅ FIXED VERSION - No Duplicate Registrations
"""
from django.contrib import admin
from .models import (
    User, Owner, Patient, MedicalRecord, Prescription,
    Vaccination, LabTest, SharedURL, Payment, 
    Subscription, AuditLog, PetPassbook
)


# ============================================================================
# USER ADMIN
# ============================================================================

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'role', 'is_active', 'date_joined']
    list_filter = ['role', 'is_active', 'is_staff']
    search_fields = ['username', 'email', 'first_name', 'last_name']
    ordering = ['-date_joined']


# ============================================================================
# OWNER ADMIN
# ============================================================================

@admin.register(Owner)
class OwnerAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone', 'email', 'city', 'created_at']
    list_filter = ['city', 'created_at']
    search_fields = ['name', 'phone', 'email']
    ordering = ['-created_at']


# ============================================================================
# PATIENT ADMIN
# ============================================================================

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ['pet_name', 'species', 'breed', 'owner', 'gender', 'is_active', 'created_at']
    list_filter = ['species', 'gender', 'is_active', 'created_at']
    search_fields = ['pet_name', 'breed', 'owner__name', 'microchip_id']
    ordering = ['-created_at']
    readonly_fields = ['qr_code']


# ============================================================================
# MEDICAL RECORD ADMIN
# ============================================================================

@admin.register(MedicalRecord)
class MedicalRecordAdmin(admin.ModelAdmin):
    list_display = ['patient', 'visit_type', 'visit_date', 'doctor', 'consultation_fee']
    list_filter = ['visit_type', 'visit_date']
    search_fields = ['patient__pet_name', 'chief_complaint', 'diagnosis']
    ordering = ['-visit_date']
    date_hierarchy = 'visit_date'


# ============================================================================
# PRESCRIPTION ADMIN (SINGLE REGISTRATION)
# ============================================================================

@admin.register(Prescription)
class PrescriptionAdmin(admin.ModelAdmin):
    list_display = ['medication_name', 'dosage', 'get_patient_name', 'frequency', 'price', 'created_at']
    list_filter = ['created_at']
    search_fields = ['medication_name', 'medical_record__patient__pet_name']
    ordering = ['-created_at']
    
    def get_patient_name(self, obj):
        if obj.medical_record and obj.medical_record.patient:
            return obj.medical_record.patient.pet_name
        return 'N/A'
    get_patient_name.short_description = 'Patient'


# ============================================================================
# VACCINATION ADMIN
# ============================================================================

@admin.register(Vaccination)
class VaccinationAdmin(admin.ModelAdmin):
    list_display = ['patient', 'vaccine_name', 'date_administered', 'next_due_date', 'certificate_number']
    list_filter = ['date_administered', 'vaccine_name']
    search_fields = ['patient__pet_name', 'vaccine_name', 'certificate_number']
    ordering = ['-date_administered']
    readonly_fields = ['certificate_number']


# ============================================================================
# LAB TEST ADMIN
# ============================================================================

@admin.register(LabTest)
class LabTestAdmin(admin.ModelAdmin):
    list_display = ['patient', 'test_name', 'test_type', 'ordered_date', 'status', 'cost']
    list_filter = ['status', 'test_type', 'ordered_date']
    search_fields = ['patient__pet_name', 'test_name']
    ordering = ['-ordered_date']


# ============================================================================
# SHARED URL ADMIN
# ============================================================================

@admin.register(SharedURL)
class SharedURLAdmin(admin.ModelAdmin):
    list_display = ['patient', 'share_type', 'short_code', 'created_at', 'expires_at', 'accessed_count']
    list_filter = ['share_type', 'created_at']
    search_fields = ['patient__pet_name', 'short_code']
    ordering = ['-created_at']
    readonly_fields = ['short_code', 'accessed_count', 'last_accessed']


# ============================================================================
# PAYMENT ADMIN
# ============================================================================

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['patient', 'amount', 'payment_method', 'payment_status', 'payment_date']
    list_filter = ['payment_method', 'payment_status', 'payment_date']
    search_fields = ['patient__pet_name', 'transaction_id']
    ordering = ['-payment_date']
    date_hierarchy = 'payment_date'


# ============================================================================
# SUBSCRIPTION ADMIN
# ============================================================================

@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ['user', 'plan', 'is_active', 'start_date', 'end_date', 'max_patients']
    list_filter = ['plan', 'is_active']
    search_fields = ['user__username', 'user__email']
    ordering = ['-created_at']


# ============================================================================
# AUDIT LOG ADMIN
# ============================================================================

@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ['user', 'action', 'model_name', 'object_id', 'timestamp']
    list_filter = ['action', 'model_name', 'timestamp']
    search_fields = ['user__username', 'model_name', 'description']
    ordering = ['-timestamp']
    date_hierarchy = 'timestamp'
    readonly_fields = ['timestamp']


# ============================================================================
# PET PASSBOOK ADMIN (NOT 'Passbook')
# ============================================================================

@admin.register(PetPassbook)
class PetPassbookAdmin(admin.ModelAdmin):
    list_display = ['patient', 'is_enabled', 'is_active_status', 'subscription_end', 'access_count']
    list_filter = ['is_enabled', 'subscription_type', 'created_at']
    search_fields = ['patient__pet_name', 'access_token']
    ordering = ['-created_at']
    readonly_fields = ['access_token', 'access_count', 'last_accessed']
    
    def is_active_status(self, obj):
        return obj.is_active
    is_active_status.short_description = 'Active'
    is_active_status.boolean = True