from django.shortcuts import render
from vouchers.models import voucher
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin
# Create your views here.
class historico(LoginRequiredMixin,PermissionRequiredMixin,ListView):
    model = voucher
    template_name ='historico.html'
    context_object_name = 'vouchers'
    permission_required = 'posto.add_posto'
    paginate_by = 10