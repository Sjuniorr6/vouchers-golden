"""
Arquivo de views para gerenciar login e logout no app 'login'.
"""

from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView

class UserLoginView(LoginView):
    """
    View responsável por exibir o formulário de login e autenticar o usuário.
    """
    template_name = "login/login.html"
    success_url = reverse_lazy("home")  # Redireciona para a rota 'home' após login bem-sucedido

class UserLogoutView(LogoutView):
    """
    View responsável por encerrar a sessão do usuário autenticado.
    """
    next_page = reverse_lazy("login")  # Redireciona para a rota 'login' após logout
