# Generated by Django 3.2.16 on 2022-11-22 20:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0007_alter_referrals_referred'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='linkedln',
            new_name='linkedin',
        ),
    ]