# Generated by Django 5.1.2 on 2025-03-11 14:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vouchers', '0005_voucher_telefone'),
    ]

    operations = [
        migrations.AddField(
            model_name='voucher',
            name='gasto',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True),
        ),
    ]
