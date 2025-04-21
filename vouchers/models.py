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

    # Campos de auditoria
    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='vouchers_updated'
    )
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Voucher {self.pk}"

    @property
    def is_expired(self):
        return (timezone.now() - self.data) > timedelta(hours=24)

    def clean(self):
        super().clean()
        gasto_atual = self.gasto or Decimal('0')

        if self.pk:
            # Atualização
            old = Voucher.objects.get(pk=self.pk)

            # Bloqueia mudanças em voucher expirado
            if self.is_expired:
                if gasto_atual != (old.gasto or Decimal('0')):
                    raise ValidationError(
                        "Não é permitido alterar gasto de um voucher expirado."
                    )
                return

            # Gasto não pode exceder o valor anterior
            if gasto_atual > old.valor:
                raise ValidationError(
                    "O gasto não pode ser maior que o valor do voucher."
                )

            # Subtrai gasto do valor anterior
            self.valor = old.valor - gasto_atual

        else:
            # Criação: gasto não pode exceder valor inicial
            if gasto_atual > self.valor:
                raise ValidationError(
                    "O gasto não pode ser maior que o valor do voucher."
                )
            self.valor = self.valor - gasto_atual

    def save(self, *args, user=None, **kwargs):
        # Registra quem alterou valor ou gasto
        if self.pk and user is not None:
            old = Voucher.objects.get(pk=self.pk)
            if (
                (self.valor != old.valor) or
                ((self.gasto or Decimal('0')) != (old.gasto or Decimal('0')))
            ):
                self.updated_by = user

        creating = self.pk is None
        self.full_clean()
        super().save(*args, **kwargs)

        # Gera QR code se for novo voucher
        if creating or not self.qrcode_image:
            domain = "http://www.gsvouchers.com.br"
            edit_url = f"{domain}/vouchers/editar/{self.pk}/"

            qr = qrcode.QRCode(version=1, box_size=10, border=4)
            qr.add_data(edit_url)
            qr.make(fit=True)

            img = qr.make_image(fill_color="black", back_color="white")
            img_io = BytesIO()
            img.save(img_io, 'PNG')
            img_io.seek(0)

            filename = f"qr_{uuid.uuid4().hex}.png"
            self.qrcode_image.save(filename, File(img_io), save=False)

            super().save(update_fields=['qrcode_image'])