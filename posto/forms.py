from django import forms
from .models import Posto

class PostoForm(forms.ModelForm):
    class Meta:
        model = Posto
        fields = ['nome', 'cidade', 'estado', 'endereco', 'gerente']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Digite o nome do posto'}),
            'cidade': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Digite a cidade'}),
            'estado': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: SP'}),
            'endereco': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Digite o endereço'}),
            'gerente': forms.Select(attrs={'class': 'form-control'}),
        }
