
from django.urls import path
from .views import VoucherListView,VoucherCreateView,VoucherDeleteView,VoucherUpdateView,voucher_activate_status
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('voucher', VoucherListView.as_view(), name='voucher'),
    path('criar/', VoucherCreateView.as_view(), name='voucher_create'),
    path('delete/<int:pk>/', VoucherDeleteView.as_view(), name='voucher_delete'),
    path('editar/<int:pk>/', VoucherUpdateView.as_view(), name='voucher_update'),  # Nova rota
    path('activate/<int:pk>/', voucher_activate_status, name='voucher_activate_status'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
