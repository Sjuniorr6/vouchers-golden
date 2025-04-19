from rest_framework import viewsets, permissions
from vouchers.models import voucher
from .serializers import VoucherSerializer

class VoucherReadOnlyViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = voucher.objects.all().order_by('-data')
    serializer_class = VoucherSerializer
    permission_classes = [permissions.AllowAny]
