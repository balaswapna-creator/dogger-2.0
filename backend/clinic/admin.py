from django.contrib import admin
from .models import (
    User, Owner, Patient, MedicalRecord, Prescription, 
    Vaccination, LabTest, SharedURL, Payment, Subscription, AuditLog
)

@admin.register(Owner)
class OwnerAdmin(admin.ModelAdmin):
    list_display = ['name', 'phone', 'email', 'city', 'created_at']
    search_fields = ['name', 'phone', 'email', 'whatsapp_number']
    list_filter = ['city', 'created_at']
    ordering = ['-created_at']

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ['pet_name', 'species', 'breed', 'owner', 'gender', 'date_of_birth', 'is_active']
    search_fields = ['pet_name', 'microchip_id', 'owner__name']
    list_filter = ['species', 'gender', 'breed', 'is_active']
    ordering = ['-created_at']
    readonly_fields = ['qr_code']

@admin.register(MedicalRecord)
class MedicalRecordAdmin(admin.ModelAdmin):
    list_display = ['patient', 'visit_date', 'visit_type', 'doctor', 'consultation_fee']
    search_fields = ['patient__pet_name', 'diagnosis', 'chief_complaint']
    list_filter = ['visit_type', 'visit_date', 'doctor']
    ordering = ['-visit_date']

@admin.register(Prescription)
class PrescriptionAdmin(admin.ModelAdmin):
    list_display = ['medical_record', 'medication_name', 'dosage', 'frequency', 'quantity', 'price']
    search_fields = ['medication_name', 'medical_record__patient__pet_name']
    list_filter = ['frequency']
    ordering = ['-created_at']

@admin.register(Vaccination)
class VaccinationAdmin(admin.ModelAdmin):
    list_display = ['patient', 'vaccine_name', 'date_administered', 'next_due_date', 'certificate_number']
    search_fields = ['vaccine_name', 'patient__pet_name', 'certificate_number']
    list_filter = ['date_administered', 'next_due_date']
    ordering = ['-date_administered']
    readonly_fields = ['certificate_number']

@admin.register(LabTest)
class LabTestAdmin(admin.ModelAdmin):
    list_display = ['patient', 'test_name', 'ordered_date', 'status', 'cost']
    search_fields = ['test_name', 'patient__pet_name']
    list_filter = ['status', 'ordered_date', 'test_type']
    ordering = ['-ordered_date']

@admin.register(SharedURL)
class SharedURLAdmin(admin.ModelAdmin):
    list_display = ['patient', 'share_type', 'short_code', 'created_at', 'expires_at', 'accessed_count']
    search_fields = ['short_code', 'patient__pet_name']
    list_filter = ['share_type', 'created_at']
    ordering = ['-created_at']
    readonly_fields = ['short_code', 'accessed_count', 'last_accessed']

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['patient', 'amount', 'payment_method', 'payment_status', 'payment_date']
    search_fields = ['patient__pet_name', 'transaction_id']
    list_filter = ['payment_status', 'payment_method', 'payment_date']
    ordering = ['-payment_date']

@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ['user', 'plan', 'is_active', 'start_date', 'end_date', 'max_patients']
    search_fields = ['user__username', 'user__email']
    list_filter = ['plan', 'is_active']
    ordering = ['-created_at']

@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ['user', 'action', 'model_name', 'timestamp', 'ip_address']
    search_fields = ['user__username', 'model_name', 'description']
    list_filter = ['action', 'model_name', 'timestamp']
    ordering = ['-timestamp']
    readonly_fields = ['user', 'action', 'model_name', 'object_id', 'timestamp', 'ip_address', 'user_agent']

# User model is already registered by Django's auth system
# If you need custom User admin, you'll need to unregister the default first:
# from django.contrib.auth.admin import UserAdmin
# admin.site.unregister(User)
# @admin.register(User)
# class CustomUserAdmin(UserAdmin):
#     pass