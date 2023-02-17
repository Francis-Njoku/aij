# Generated by Django 3.2.16 on 2023-02-11 13:14

import authentication.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0011_delete_sponsor'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('next_of_kin', models.CharField(max_length=255, null=True)),
                ('nin', models.EmailField(db_index=True, max_length=255, unique=True)),
                ('dob', models.DateField(null=True)),
                ('identity', models.ImageField(default='identity/default.jpg', upload_to=authentication.models.identity_to, verbose_name='Identity')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='profile_authentication_set', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]