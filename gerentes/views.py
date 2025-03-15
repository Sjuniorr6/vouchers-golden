from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView, CreateView
from django.urls import reverse_lazy
from .models import Gerente
from .forms import GerenteForm
from django.contrib.auth.mixins import LoginRequiredMixin,PermissionRequiredMixin

class GerenteListView(LoginRequiredMixin,PermissionRequiredMixin,ListView):
    model = Gerente
    template_name = 'gerente_list.html'
    context_object_name = 'gerentes'
    permission_required = 'gerentes.add_gerente'

class GerenteCreateView(LoginRequiredMixin,PermissionRequiredMixin,CreateView):
    model = Gerente
    form_class = GerenteForm
    template_name = 'gerente_create.html'
    success_url = reverse_lazy('gerente_list')
    permission_required = 'gerentes.add_gerente'
