# Generated by Django 3.2.16 on 2022-11-27 10:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0008_rename_linkedln_user_linkedin'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_vendor',
            field=models.BooleanField(default=False),
        ),
    ]