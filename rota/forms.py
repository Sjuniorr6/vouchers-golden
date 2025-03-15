from django import forms
from .models import Rota

class RotaForm(forms.ModelForm):
    class Meta:
        model = Rota
        fields = ['nome', 'postos']
        widgets = {
            'nome': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Digite o nome da rota'
            }),
            'postos': forms.CheckboxSelectMultiple(attrs={
                'class': 'form-check-input'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Se desejar aplicar classes a todos os campos (exceto os que já estão configurados)
        for field_name, field in self.fields.items():
            if field.widget.__class__.__name__ != 'CheckboxSelectMultiple':
                field.widget.attrs.setdefault('class', 'form-control')
