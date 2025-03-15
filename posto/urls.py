from django.urls import path
from .views import PostoListView, PostoCreateView

urlpatterns = [
    path('postos', PostoListView.as_view(), name='posto_list'),
    path('novo/', PostoCreateView.as_view(), name='posto_create'),
]
