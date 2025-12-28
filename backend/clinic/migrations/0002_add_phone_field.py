from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
        ('clinic', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='phone',
            field=models.CharField(blank=True, max_length=15, default=''),
            preserve_default=False,
        ),
    ]