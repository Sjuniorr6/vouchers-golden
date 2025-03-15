from django.urls import path
from .views import GerenteListView, GerenteCreateView

urlpatterns = [
    path('gerente/', GerenteListView.as_view(), name='gerente_list'),
    path('criar/', GerenteCreateView.as_view(), name='gerente_create'),
]
