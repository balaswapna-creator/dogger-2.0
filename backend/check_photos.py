import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dogger.settings')
django.setup()

from clinic.models import Patient

print("Checking patient photos:\n")
for p in Patient.objects.all():
    print(f"Patient: {p.name}")
    print(f"  Photo field: '{p.photo}'")
    if p.photo:
        print(f"  Photo name: {p.photo.name}")
        try:
            print(f"  Photo URL: {p.photo.url}")
        except:
            print("  Photo URL: Error generating URL")
    else:
        print("  No photo uploaded")
    print()