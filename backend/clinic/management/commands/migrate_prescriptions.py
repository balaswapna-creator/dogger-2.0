from django.core.management.base import BaseCommand
from clinic.models import Prescription

class Command(BaseCommand):
    help = 'Migrate old prescription format to new medicines array format'

    def handle(self, *args, **options):
        prescriptions = Prescription.objects.filter(medicines=[])
        count = 0
        
        for prescription in prescriptions:
            if prescription.medication_name:
                # Convert old format to new array format
                prescription.medicines = [{
                    'medication_name': prescription.medication_name,
                    'dosage': prescription.dosage,
                    'frequency': prescription.frequency,
                    'duration': prescription.duration,
                    'instructions': prescription.instructions
                }]
                prescription.save()
                count += 1
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully migrated {count} prescriptions')
        )