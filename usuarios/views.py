from django.shortcuts import render

# Create your views here.
# usuarios/views.py

from django.views.generic import CreateView, ListView
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from .models import UserProfile
from .forms import UserProfileCreationForm

class UserCreateView(CreateView):
    model = UserProfile
    form_class = UserProfileCreationForm
    template_name = 'user_create.html'
    success_url = reverse_lazy('user_list')

class UserListView(ListView):
    model = UserProfile
    template_name = 'user_list.html'
    context_object_name = 'profiles'


# usuarios/views.py

from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.models import User
from django.contrib.auth.forms import AdminPasswordChangeForm
from django.contrib import messages

def admin_password_change(request, pk):
    """
    View para um administrador alterar a senha de um usuário específico.
    """
    user = get_object_or_404(User, pk=pk)

    if request.method == 'POST':
        form = AdminPasswordChangeForm(user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Senha alterada com sucesso.')
            return redirect('user_list')  # ou outra rota de sua preferência
    else:
        form = AdminPasswordChangeForm(user)

    return render(request, 'change_password.html', {
        'form': form,
        'usuario': user
    })
