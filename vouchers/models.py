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
        """
        1) Valida e salva inicialmente para ter self.pk
        2) Gera o QR code caso seja um novo objeto ou não tenha qrcode_image
        3) Salva novamente só atualizando o campo qrcode_image
        """
        criando = self.pk is None  # Verifica se é criação de um novo voucher
        self.full_clean()          # Executa as validações do clean()
        
        super().save(*args, **kwargs)  # Salva para garantir self.pk

        # Gera o QR Code se for um novo voucher ou se ainda não tiver qrcode_image
        if criando or not self.qrcode_image:
            domain = "http://www.gsvouchers.com.br"  # Ajuste conforme seu ambiente
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

            # Salva novamente somente o campo qrcode_image
            super().save(update_fields=['qrcode_image'])
