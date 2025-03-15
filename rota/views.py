from django.shortcuts import render

# Create your views here.
# rota/views.py

from django.views.generic import CreateView, ListView
from django.urls import reverse_lazy
from .models import Rota
from .forms import RotaForm
from django.contrib.auth.mixins import PermissionRequiredMixin,LoginRequiredMixin


class RotaCreateView(LoginRequiredMixin,PermissionRequiredMixin,CreateView):
    model = Rota
    form_class = RotaForm
    template_name = 'rota_form.html'
    success_url = reverse_lazy('rota_list')
    permission_required ='rota.add_rota'

class RotaListView(LoginRequiredMixin,PermissionRequiredMixin,ListView):
    model = Rota
    template_name = 'rota_list.html'
    context_object_name = 'rotas'
    permission_required ='rota.add_rota'
