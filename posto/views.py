from django.shortcuts import render

# Create your views here.
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView
from .models import Posto
from .forms import PostoForm
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

class PostoListView(LoginRequiredMixin,PermissionRequiredMixin,ListView):
    model = Posto
    template_name = 'posto_list.html'
    context_object_name = 'postos'
    permission_required = 'posto.add_posto'



class PostoCreateView(LoginRequiredMixin,PermissionRequiredMixin,CreateView):
    form_class = PostoForm
    template_name = 'posto_form.html'
    success_url = reverse_lazy('posto_list')
    permission_required = 'posto.add_posto'