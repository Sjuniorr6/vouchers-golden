from django import forms
from django.contrib.auth.models import User
from .models import UserProfile

class UserProfileCreationForm(forms.ModelForm):
    # Campos para criar o User
    username = forms.CharField(
        label="Nome de Usuário",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )
    password = forms.CharField(
        label="Senha",
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = UserProfile
        # Incluímos apenas o campo 'rotas' do UserProfile; o campo user será criado manualmente.
        fields = ['rotas']
        widgets = {
            'rotas': forms.SelectMultiple(attrs={'class': 'form-control'}),
        }

    def save(self, commit=True):
        # 1. Cria o objeto User com base nos dados do formulário
        user = User.objects.create_user(
            username=self.cleaned_data['username'],
            email=self.cleaned_data['email'],
            password=self.cleaned_data['password']
        )
        # 2. Cria o UserProfile associado, sem salvar ainda
        profile = super().save(commit=False)
        profile.user = user  # Associa o novo usuário ao perfil

        if commit:
            profile.save()
            # Salva as relações ManyToMany (campo 'rotas')
            self.save_m2m()

        return profile
