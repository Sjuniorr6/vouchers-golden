# Generated by Django 5.1.7 on 2025-03-14 19:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vouchers', '0006_voucher_gasto'),
    ]

    operations = [
        migrations.AddField(
            model_name='voucher',
            name='status',
            field=models.CharField(blank=True, default='Pendente', max_length=50, null=True),
        ),
    ]
