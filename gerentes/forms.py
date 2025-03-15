from django import forms
from .models import Gerente

class GerenteForm(forms.ModelForm):
    class Meta:
        model = Gerente
        fields = ['nome', 'email']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }
