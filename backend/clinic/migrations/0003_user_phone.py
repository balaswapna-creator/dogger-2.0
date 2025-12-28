from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clinic', '0002_alter_patient_created_by'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='phone',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
    ]