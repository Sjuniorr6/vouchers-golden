from django import forms
from .models import voucher

class VoucherForm(forms.ModelForm):
    class Meta:
        model = voucher
        fields = ['motorista', 'placa', 'embarcador', 'telefone', 'rota', 'valor']
        widgets = {
            'motorista': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome do motorista'}),
            'placa': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Placa'}),
            'embarcador': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome do embarcador'}),
            'telefone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '55 (11) 123456789'
            }),
            # Supondo que "rota" seja um campo de relacionamento (ForeignKey ou ManyToMany),
            # você pode usar um widget Select ou SelectMultiple conforme o caso:
            'rota': forms.Select(attrs={'class': 'form-control'}),
            'valor': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
        }
# forms.py
from django import forms
from .models import voucher

# forms.py
from django import forms
from .models import voucher

class VoucherUpdateForm(forms.ModelForm):
    class Meta:
        model = voucher
        fields = ['valor', 'gasto', 'status']
        widgets = {
            'valor': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'lang': 'en'  # Aceita ponto decimal
            }),
            'gasto': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'lang': 'en'
            }),
            'status': forms.TextInput(attrs={
                'class': 'form-control',
            }),
        }
