# Generated by Django 3.2.16 on 2023-01-16 00:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('investment', '0029_investment_periodic_payment'),
    ]

    operations = [
        migrations.AddField(
            model_name='investment',
            name='off_plan',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='investment',
            name='only_returns',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='investment',
            name='outright_purchase',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='investment',
            name='outright_purchase_amount',
            field=models.IntegerField(null=True),
        ),
        migrations.CreateModel(
            name='Installment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField(null=True)),
                ('serialkey', models.CharField(max_length=255, null=True)),
                ('is_approved', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('approved_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='approved_by_installment', to=settings.AUTH_USER_MODEL)),
                ('investor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='investor_instalmment', to='investment.investors')),
            ],
        ),
    ]