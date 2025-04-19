from rest_framework.routers import DefaultRouter
from .views import VoucherReadOnlyViewSet

router = DefaultRouter()
router.register(r'vouchers', VoucherReadOnlyViewSet, basename='voucher')

urlpatterns = router.urls
