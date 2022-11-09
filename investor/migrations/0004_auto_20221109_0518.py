# Generated by Django 3.2.16 on 2022-11-09 05:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('investor', '0003_auto_20221109_0509'),
    ]

    operations = [
        migrations.AddField(
            model_name='expectations',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='created_by_expectations_set', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='investmentsize',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='created_by_size_set', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='period',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='created_by_period_set', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='risk',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='created_by_risk_set', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='interest',
            name='created_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='created_by_investor_set', to=settings.AUTH_USER_MODEL),
        ),
    ]