# rota/urls.py

from django.urls import path
from .views import RotaCreateView, RotaListView

urlpatterns = [
    path('rota', RotaListView.as_view(), name='rota_list'),      # Listar rotas
    path('novo/rota/', RotaCreateView.as_view(), name='rota_create'),  # Criar nova rota
]
