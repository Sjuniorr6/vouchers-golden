# Generated by Django 5.1.7 on 2025-03-11 13:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vouchers', '0004_remove_voucher_qrcode'),
    ]

    operations = [
        migrations.AddField(
            model_name='voucher',
            name='telefone',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
