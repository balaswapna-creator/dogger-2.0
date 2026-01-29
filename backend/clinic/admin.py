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

# File: backend/clinic/admin.py
# Update the PrescriptionAdmin class

from django.contrib import admin
from .models import Prescription

@admin.register(Prescription)
class PrescriptionAdmin(admin.ModelAdmin):
    list_display = [
        'id',
        'patient_name',
        'medicine_count',
        'created_at',
        'updated_at'
    ]
    
    list_filter = ['created_at', 'updated_at']
    
    search_fields = [
        'medical_record__patient__pet_name',
        'medication_name',
        'medicines'
    ]
    
    readonly_fields = ['id', 'created_at', 'updated_at']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('id', 'medical_record')
        }),
        ('Medicines', {
            'fields': ('medicines',),
            'description': 'List of medicines in JSON format'
        }),
        ('Legacy Fields (Backward Compatibility)', {
            'fields': (
                'medication_name',
                'dosage',
                'frequency',
                'duration',
                'instructions'
            ),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        })
    )
    
    def patient_name(self, obj):
        """Display patient name"""
        return obj.patient_name
    patient_name.short_description = 'Patient'
    
    def medicine_count(self, obj):
        """Display number of medicines"""
        return obj.medicine_count
    medicine_count.short_description = '# Medicines'

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