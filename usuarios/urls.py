# usuarios/urls.py

from django.urls import path
from .views import UserCreateView, UserListView,admin_password_change

urlpatterns = [
    path('create/', UserCreateView.as_view(), name='user_create'),
    path('list/', UserListView.as_view(), name='user_list'),
      path('change_password/<int:pk>/', admin_password_change, name='user_change_password'),
]
