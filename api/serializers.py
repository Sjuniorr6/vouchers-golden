from rest_framework import serializers
from vouchers.models import voucher

class VoucherSerializer(serializers.ModelSerializer):
    class Meta:
        model = voucher
        fields = '__all__'
