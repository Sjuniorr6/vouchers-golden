# models.py
from django.db import models
from django.core.exceptions import ValidationError
from django.core.files import File
from django.conf import settings
from rota.models import Rota
import uuid
import qrcode
from io import BytesIO
from datetime import timedelta
from django.utils import timezone

class voucher(models.Model):
    motorista = models.CharField(max_length=50, null=True, blank=True)
    data = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    placa = models.CharField(max_length=50, null=True, blank=True)
    embarcador = models.CharField(max_length=50, null=True, blank=True)
    telefone = models.CharField(max_length=50, null=True, blank=True)
    status = models.CharField(max_length=50, null=True, blank=True, default='Pendente')
    gasto = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    rota = models.ForeignKey(Rota, on_delete=models.SET_NULL, null=True, blank=True)
    valor = models.DecimalField(max_digits=6, decimal_places=2, default=40.00)
    qrcode_image = models.ImageField(upload_to='qrcodes', null=True, blank=True)

    def __str__(self):
        return f"Voucher {self.pk}"

    @property
    def is_expired(self):
        return (timezone.now() - self.data) > timedelta(hours=24)

    def clean(self):
        super().clean()
        if self.pk:
            old_instance = voucher.objects.get(pk=self.pk)
            if self.is_expired:
                # Bloqueia qualquer alteração se expirado
                if (self.valor != old_instance.valor) or (self.gasto != old_instance.gasto):
                    raise ValidationError("Não é permitido alterar o valor ou o gasto de um voucher expirado.")
            else:
                # Não expirado -> não pode aumentar valor, nem ficar negativo
                old_valor = old_instance.valor
                if self.valor > old_valor:
                    raise ValidationError("Não é permitido aumentar o valor do voucher.")
                
                gasto_atual = self.gasto or 0
                novo_valor = old_valor - gasto_atual
                if novo_valor < 0:
                    raise ValidationError("O valor não pode ficar negativo após subtrair o gasto.")
                
                # Ajusta 'valor' de acordo com o gasto
                self.valor = novo_valor

        else:
            # Criação de novo voucher
            gasto_atual = self.gasto or 0
            novo_valor = self.valor - gasto_atual
            if novo_valor < 0:
                raise ValidationError("O valor não pode ficar negativo na criação.")
            self.valor = novo_valor

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
        # (QR code logic permanece igual)
