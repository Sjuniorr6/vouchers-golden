# vouchers/urls.py
from django.urls import path
from .views import VoucherDashboardView,download_excel_report,download_pdf_report

urlpatterns = [
    # ... outras URLs ...
    path('dashboard/', VoucherDashboardView.as_view(), name='voucher_dashboard'),
     path('download/excel/', download_excel_report, name='download_excel_report'),
    path('download/pdf/', download_pdf_report, name='download_pdf_report'),
]
