# Generated by Django 5.0.4 on 2024-11-04 16:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('resume', '0003_remove_jobexperience_profile_jobexperience_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='education',
            field=models.JSONField(blank=True, null=True),
        ),
    ]