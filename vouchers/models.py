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
from decimal import Decimal
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
    valor = models.DecimalField(max_digits=6, decimal_places=2, default=Decimal('40.00'))
    qrcode_image = models.ImageField(upload_to='qrcodes', null=True, blank=True)

    # auditoria
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='vouchers_updated'
    )
    updated_at = models.DateTimeField(auto_now=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # guarda valores originais para evitar dupla subtração
        self._initial_valor = self.valor
        self._initial_gasto = self.gasto or Decimal('0')

    def __str__(self):
        return f"Voucher {self.pk}"

    @property
    def is_expired(self):
        return (timezone.now() - self.data) > timedelta(hours=24)

    def clean(self):
        super().clean()
        gasto_atual = self.gasto or Decimal('0')

        # não permite gastar mais que o valor base
        if gasto_atual > self._initial_valor:
            raise ValidationError("O gasto não pode ser maior que o valor do voucher.")

        # se expirado, bloqueia alterações de gasto
        if self.pk and self.is_expired:
            if gasto_atual != self._initial_gasto:
                raise ValidationError("Não é permitido alterar o gasto de um voucher expirado.")
            return

        # calcula valor restante a partir do valor inicial
        self.valor = self._initial_valor - gasto_atual

        if self.valor < 0:
            raise ValidationError("O valor não pode ficar negativo após subtrair o gasto.")

    def save(self, *args, user=None, **kwargs):
        # registra usuário em alteração de gasto/valor
        if self.pk and user is not None:
            if (self.valor != self._initial_valor) or ((self.gasto or Decimal('0')) != self._initial_gasto):
                self.updated_by = user

        creating = self.pk is None
        self.full_clean()
        super().save(*args, **kwargs)

        # gera QR code para novos
        if creating or not self.qrcode_image:
            domain = "http://www.gsvouchers.com.br"
            link = f"{domain}/vouchers/editar/{self.pk}/"
            qr = qrcode.QRCode(version=1, box_size=10, border=4)
            qr.add_data(link)
            qr.make(fit=True)

            img = qr.make_image(fill_color="black", back_color="white")
            buf = BytesIO()
            img.save(buf, 'PNG')
            buf.seek(0)
            name = f"qr_{uuid.uuid4().hex}.png"
            self.qrcode_image.save(name, File(buf), save=False)
            super().save(update_fields=['qrcode_image'])
