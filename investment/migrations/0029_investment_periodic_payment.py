# Generated by Django 3.2.16 on 2022-12-29 05:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('investment', '0028_auto_20221228_0331'),
    ]

    operations = [
        migrations.AddField(
            model_name='investment',
            name='periodic_payment',
            field=models.DecimalField(decimal_places=2, default=1, max_digits=6),
        ),
    ]
