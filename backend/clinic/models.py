"""
Dogger 2.0 - Complete Django Models with Table Prefixes
Sri Adithya Pet Clinic Management System
✅ FIXED VERSION - QR Code Issue Resolved
"""

from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator, MinValueValidator
from django.utils import timezone
from datetime import timedelta
import uuid
import qrcode
from io import BytesIO
from django.core.files import File

# ============================================================================
# USER & AUTHENTICATION
# ============================================================================

class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    role = models.CharField(max_length=20, choices=[
        ('admin', 'Admin'),
        ('doctor', 'Doctor'),
        ('staff', 'Staff'),
    ])
    phone = models.CharField(max_length=15, blank=True, null=True)
    
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to.',
        related_name='dogger_users',
        related_query_name='dogger_user',
    )
    
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name='dogger_users',
        related_query_name='dogger_user',
    )
    
    class Meta:
        db_table = 'dogger_users'

    def __str__(self):
        return self.username


# ============================================================================
# OWNER & PATIENT
# ============================================================================

class Owner(models.Model):
    """Pet owner/client information"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=15, db_index=True)
    email = models.EmailField(blank=True)
    address = models.TextField(blank=True)
    city = models.CharField(max_length=100, default='Cumbum')
    whatsapp_number = models.CharField(max_length=15, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='owners_created')

    class Meta:
        db_table = 'dogger_owners'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['phone']),
            models.Index(fields=['name']),
        ]

    def __str__(self):
        return f"{self.name} - {self.phone}"


class Patient(models.Model):
    """Pet/Patient information"""
    SPECIES_CHOICES = [
        ('dog', 'Dog'),
        ('cat', 'Cat'),
        ('bird', 'Bird'),
        ('rabbit', 'Rabbit'),
        ('other', 'Other'),
    ]

    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    pet_name = models.CharField(max_length=100)
    species = models.CharField(max_length=20, choices=SPECIES_CHOICES)
    breed = models.CharField(max_length=100, blank=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    date_of_birth = models.DateField(null=True, blank=True)
    color = models.CharField(max_length=50, blank=True)
    microchip_id = models.CharField(max_length=50, blank=True, unique=True, null=True)
    photo = models.ImageField(
        upload_to='patients/photos/',
        blank=True,
        null=True,
        validators=[FileExtensionValidator(['jpg', 'jpeg', 'png', 'webp'])]
    )
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE, related_name='patients')
    qr_code = models.ImageField(upload_to='patients/qr/', blank=True, null=True)
    allergies = models.TextField(blank=True)
    chronic_conditions = models.TextField(blank=True)
    current_medications = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    last_visit = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='patients_created')    

    class Meta:
        db_table = 'dogger_patients'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['pet_name']),
            models.Index(fields=['species']),
            models.Index(fields=['owner']),
        ]

    def __str__(self):
        return f"{self.pet_name} ({self.species}) - {self.owner.name}"

    def save(self, *args, **kwargs):
        """✅ FIXED: Generate QR code without infinite recursion"""
        is_new = self.pk is None
        
        # Save first to get the ID
        super().save(*args, **kwargs)
        
        # Generate QR code only for new patients without QR
        if is_new and not self.qr_code:
            try:
                qr_data = f"https://dogger.clinic/passbook/{self.id}"
                qr = qrcode.QRCode(version=1, box_size=10, border=2)
                qr.add_data(qr_data)
                qr.make(fit=True)
                img = qr.make_image(fill_color="#226C3B", back_color="white")
                
                buffer = BytesIO()
                img.save(buffer, format='PNG')
                buffer.seek(0)  # ✅ CRITICAL FIX: Reset buffer position
                
                filename = f'qr_{self.id}.png'
                # ✅ Use save=False to avoid recursion
                self.qr_code.save(filename, File(buffer), save=False)
                
                # ✅ Update only the qr_code field
                super().save(update_fields=['qr_code'])
            except Exception as e:
                # Don't crash patient creation if QR fails
                print(f"⚠️ QR code generation failed for patient {self.id}: {e}")

    @property
    def age_string(self):
        if not self.date_of_birth:
            return "Unknown"
        today = timezone.now().date()
        years = today.year - self.date_of_birth.year
        months = today.month - self.date_of_birth.month
        if months < 0:
            years -= 1
            months += 12
        if years > 0:
            return f"{years} year{'s' if years > 1 else ''}"
        return f"{months} month{'s' if months > 1 else ''}"


# ============================================================================
# MEDICAL RECORDS
# ============================================================================

class MedicalRecord(models.Model):
    """Individual consultation/visit record"""
    VISIT_TYPE_CHOICES = [
        ('consultation', 'General Consultation'),
        ('vaccination', 'Vaccination'),
        ('surgery', 'Surgery'),
        ('emergency', 'Emergency'),
        ('followup', 'Follow-up'),
        ('grooming', 'Grooming'),
        ('lab', 'Lab Test'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='medical_records')
    visit_date = models.DateTimeField(default=timezone.now)
    visit_type = models.CharField(max_length=20, choices=VISIT_TYPE_CHOICES, default='consultation')
    chief_complaint = models.TextField()
    history = models.TextField(blank=True)
    clinical_notes = models.TextField(blank=True)
    diagnosis = models.TextField(blank=True)
    treatment_plan = models.TextField(blank=True)
    temperature = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True)
    weight = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    heart_rate = models.IntegerField(null=True, blank=True)
    next_visit_date = models.DateField(null=True, blank=True)
    follow_up_notes = models.TextField(blank=True)
    consultation_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    doctor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='consultations')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'dogger_medical_records'
        ordering = ['-visit_date']
        indexes = [
            models.Index(fields=['patient', '-visit_date']),
            models.Index(fields=['visit_type']),
        ]

    def __str__(self):
        return f"{self.patient.pet_name} - {self.visit_type} - {self.visit_date.date()}"


# ============================================================================
# PRESCRIPTION
# ============================================================================

class Prescription(models.Model):
    """Prescription linked to a medical record"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    medical_record = models.ForeignKey(MedicalRecord, on_delete=models.CASCADE, related_name='prescriptions')
    medication_name = models.CharField(max_length=200)
    dosage = models.CharField(max_length=100)
    frequency = models.CharField(max_length=100)
    duration = models.CharField(max_length=100)
    instructions = models.TextField(blank=True)
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'dogger_prescriptions'
        ordering = ['medication_name']

    def __str__(self):
        return f"{self.medication_name} - {self.dosage}"


# ============================================================================
# VACCINATIONS
# ============================================================================

class Vaccination(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='vaccinations')
    vaccine_name = models.CharField(max_length=100)
    manufacturer = models.CharField(max_length=200, blank=True, null=True)
    batch_number = models.CharField(max_length=100, blank=True, null=True)
    date_administered = models.DateField()
    next_due_date = models.DateField(blank=True, null=True)
    administered_by = models.CharField(max_length=200, blank=True, null=True)
    certificate_number = models.CharField(max_length=50, unique=True, editable=False)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'dogger_vaccinations'
        ordering = ['-date_administered']
    
    def save(self, *args, **kwargs):
        if not self.certificate_number:
            last_vax = Vaccination.objects.order_by('-id').first()
            if last_vax and last_vax.certificate_number:
                try:
                    last_num = int(last_vax.certificate_number.replace('VAX', ''))
                    self.certificate_number = f'VAX{str(last_num + 1).zfill(8)}'
                except:
                    self.certificate_number = f'VAX{str(Vaccination.objects.count() + 1).zfill(8)}'
            else:
                self.certificate_number = 'VAX00000001'
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f'{self.vaccine_name} - {self.patient.pet_name}'


# ============================================================================
# LAB TESTS
# ============================================================================

class LabTest(models.Model):
    """Laboratory test record"""
    TEST_STATUS = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='lab_tests')
    medical_record = models.ForeignKey(MedicalRecord, on_delete=models.SET_NULL, null=True, blank=True, related_name='lab_tests')
    test_name = models.CharField(max_length=200)
    test_type = models.CharField(max_length=100, blank=True)
    ordered_date = models.DateTimeField(default=timezone.now)
    sample_collected_date = models.DateTimeField(null=True, blank=True)
    result_date = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=TEST_STATUS, default='pending')
    result_values = models.JSONField(default=dict, blank=True)
    result_notes = models.TextField(blank=True)
    result_file = models.FileField(upload_to='lab/results/', blank=True, null=True)
    ordered_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='lab_tests_ordered')
    performed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='lab_tests_performed')
    cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'dogger_lab_tests'
        ordering = ['-ordered_date']
        indexes = [
            models.Index(fields=['patient', '-ordered_date']),
            models.Index(fields=['status']),
        ]

    def __str__(self):
        return f"{self.patient.pet_name} - {self.test_name} - {self.status}"


# ============================================================================
# SHARED URLS
# ============================================================================

class SharedURL(models.Model):
    """Short-lived signed URLs for sharing"""
    SHARE_TYPE_CHOICES = [
        ('passbook', 'Health Passbook'),
        ('prescription', 'Prescription PDF'),
        ('vaccination', 'Vaccination Certificate'),
        ('health_cert', 'Health Certificate'),
        ('lab_report', 'Lab Report'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='shared_urls')
    share_type = models.CharField(max_length=20, choices=SHARE_TYPE_CHOICES)
    short_code = models.CharField(max_length=12, unique=True, db_index=True)
    reference_id = models.UUIDField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()
    accessed_count = models.IntegerField(default=0)
    last_accessed = models.DateTimeField(null=True, blank=True)
    ip_addresses = models.JSONField(default=list, blank=True)

    class Meta:
        db_table = 'dogger_shared_urls'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['short_code']),
            models.Index(fields=['expires_at']),
        ]

    def save(self, *args, **kwargs):
        if not self.short_code:
            self.short_code = uuid.uuid4().hex[:12]
        if not self.expires_at:
            self.expires_at = timezone.now() + timedelta(minutes=30)
        super().save(*args, **kwargs)

    @property
    def is_valid(self):
        return timezone.now() < self.expires_at

    def __str__(self):
        return f"{self.share_type} - {self.short_code}"


# ============================================================================
# PAYMENTS
# ============================================================================

class Payment(models.Model):
    """Payment/billing records"""
    PAYMENT_METHOD = [
        ('cash', 'Cash'),
        ('card', 'Card'),
        ('upi', 'UPI'),
        ('bank_transfer', 'Bank Transfer'),
    ]

    PAYMENT_STATUS = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='payments')
    medical_record = models.ForeignKey(MedicalRecord, on_delete=models.SET_NULL, null=True, blank=True, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD, default='cash')
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS, default='pending')
    transaction_id = models.CharField(max_length=100, blank=True)
    consultation_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    medication_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    lab_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    other_charges = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    notes = models.TextField(blank=True)
    payment_date = models.DateTimeField(default=timezone.now)
    received_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='payments_received')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'dogger_payments'
        ordering = ['-payment_date']
        indexes = [
            models.Index(fields=['patient', '-payment_date']),
            models.Index(fields=['payment_status']),
        ]

    def __str__(self):
        return f"{self.patient.pet_name} - ₹{self.amount} - {self.payment_status}"


# ============================================================================
# SUBSCRIPTIONS
# ============================================================================

class Subscription(models.Model):
    """Clinic subscription"""
    PLAN_CHOICES = [
        ('free', 'Free'),
        ('basic', 'Basic'),
        ('premium', 'Premium'),
        ('enterprise', 'Enterprise'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='subscription')
    plan = models.CharField(max_length=20, choices=PLAN_CHOICES, default='free')
    is_active = models.BooleanField(default=True)
    start_date = models.DateTimeField(default=timezone.now)
    end_date = models.DateTimeField(null=True, blank=True)
    max_patients = models.IntegerField(default=50)
    pdf_exports_limit = models.IntegerField(default=10)
    voice_transcriptions_limit = models.IntegerField(default=20)
    current_pdf_exports = models.IntegerField(default=0)
    current_voice_uses = models.IntegerField(default=0)
    last_reset = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'dogger_subscriptions'

    def __str__(self):
        return f"{self.user.username} - {self.plan}"

    def reset_monthly_limits(self):
        self.current_pdf_exports = 0
        self.current_voice_uses = 0
        self.last_reset = timezone.now()
        self.save()


# ============================================================================
# AUDIT LOGS
# ============================================================================

class AuditLog(models.Model):
    """Track important actions"""
    ACTION_CHOICES = [
        ('create', 'Created'),
        ('update', 'Updated'),
        ('delete', 'Deleted'),
        ('view', 'Viewed'),
        ('share', 'Shared'),
        ('export', 'Exported'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='audit_logs')
    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    model_name = models.CharField(max_length=100)
    object_id = models.UUIDField()
    description = models.TextField(blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        db_table = 'dogger_audit_logs'
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['-timestamp']),
            models.Index(fields=['model_name', 'object_id']),
        ]

    def __str__(self):
        return f"{self.user} - {self.action} - {self.model_name} - {self.timestamp}"


# ============================================================================
# PET PASSBOOK
# ============================================================================

class PetPassbook(models.Model):
    """Digital Pet Passbook with QR access"""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    patient = models.OneToOneField(Patient, on_delete=models.CASCADE, related_name='passbook')
    access_token = models.UUIDField(default=uuid.uuid4, unique=True, db_index=True)
    is_enabled = models.BooleanField(default=False)
    subscription_start = models.DateTimeField(null=True, blank=True)
    subscription_end = models.DateTimeField(null=True, blank=True)
    subscription_type = models.CharField(
        max_length=20,
        choices=[('monthly', 'Monthly'), ('yearly', 'Yearly')],
        default='monthly'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_accessed = models.DateTimeField(null=True, blank=True)
    access_count = models.IntegerField(default=0)
    
    class Meta:
        db_table = 'dogger_pet_passbooks'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Passbook for {self.patient.pet_name}"
    
    @property
    def is_active(self):
        if not self.is_enabled:
            return False
        if not self.subscription_end:
            return False
        return timezone.now() <= self.subscription_end
    
    @property
    def days_remaining(self):
        if not self.subscription_end:
            return 0
        delta = self.subscription_end - timezone.now()
        return max(0, delta.days)
    
    def regenerate_token(self):
        self.access_token = uuid.uuid4()
        self.save()
        return self.access_token
    
    def activate_subscription(self, duration_months=1):
        now = timezone.now()
        if self.subscription_end and self.subscription_end > now:
            self.subscription_end = self.subscription_end + timedelta(days=30 * duration_months)
        else:
            self.subscription_start = now
            self.subscription_end = now + timedelta(days=30 * duration_months)
        self.is_enabled = True
        self.save()
    
    def record_access(self):
        self.last_accessed = timezone.now()
        self.access_count += 1
        self.save(update_fields=['last_accessed', 'access_count'])