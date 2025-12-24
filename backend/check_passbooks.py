import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dogger.settings')
django.setup()

from clinic.models import PetPassbook, Patient

print(f"📊 Total passbooks: {PetPassbook.objects.count()}")
print(f"📊 Total patients: {Patient.objects.count()}")

print("\n📋 Passbooks:")
for pb in PetPassbook.objects.all():
    print(f"  - {pb.patient.pet_name}: enabled={pb.is_enabled}, active={pb.is_active}")
    print(f"    Token: {pb.access_token}")
    print(f"    Created: {pb.created_at}")
    
print("\n📋 Patients without passbooks:")
patients_with_passbooks = PetPassbook.objects.values_list('patient_id', flat=True)
patients_without = Patient.objects.exclude(id__in=patients_with_passbooks)
for p in patients_without:
    print(f"  - {p.pet_name} (ID: {p.id})")